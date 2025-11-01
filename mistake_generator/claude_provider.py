"""
Claude AI 提供者实现
使用 Anthropic API
"""
import json
from typing import Dict, Any, Optional
from pathlib import Path
from anthropic import Anthropic
from .ai_provider import AIProvider


class ClaudeProvider(AIProvider):
    """Claude AI 提供者"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4.5-20250929"):
        """
        初始化 Claude 提供者

        Args:
            api_key: Anthropic API 密钥
            model: Claude 模型名称
        """
        super().__init__(api_key, model)
        self.client = Anthropic(api_key=api_key)

    def analyze_image(
        self,
        image_path: Path,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        使用 Claude Vision API 分析图像

        Args:
            image_path: 图像路径
            prompt: 用户提示词
            system_prompt: 系统提示词（可选）

        Returns:
            AI 的文本响应
        """
        # 编码图像
        image_data = self.encode_image(image_path)
        media_type = self.get_image_mime_type(image_path)

        # 构建消息
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ]

        # 调用 API
        kwargs = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": messages,
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.client.messages.create(**kwargs)

        # 提取文本响应
        return response.content[0].text

    def text_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        Claude 文本生成

        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词（可选）
            temperature: 温度参数
            max_tokens: 最大 token 数

        Returns:
            AI 的文本响应
        """
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages,
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.client.messages.create(**kwargs)

        return response.content[0].text

    def structured_output(
        self,
        prompt: str,
        response_format: Dict[str, Any],
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Claude 结构化输出（通过提示词引导 JSON 格式）

        Args:
            prompt: 用户提示词
            response_format: 期望的响应格式（示例）
            system_prompt: 系统提示词（可选）

        Returns:
            结构化的 JSON 数据
        """
        # Claude 不直接支持 JSON 模式，通过提示词引导
        json_prompt = f"""{prompt}

请以 JSON 格式返回结果，格式示例：
{json.dumps(response_format, ensure_ascii=False, indent=2)}

只返回 JSON，不要包含任何其他文本。"""

        response_text = self.text_completion(
            prompt=json_prompt,
            system_prompt=system_prompt,
            temperature=0.3  # 降低温度以提高准确性
        )

        # 尝试解析 JSON
        try:
            # 清理可能的 markdown 代码块标记
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            return json.loads(response_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"无法解析 Claude 返回的 JSON: {e}\n原始响应: {response_text}")
