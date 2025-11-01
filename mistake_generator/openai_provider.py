"""
OpenAI 提供者实现
使用 OpenAI API
"""
import json
from typing import Dict, Any, Optional
from pathlib import Path
from openai import OpenAI
from .ai_provider import AIProvider


class OpenAIProvider(AIProvider):
    """OpenAI 提供者"""

    def __init__(self, api_key: str, model: str = "gpt-4o"):
        """
        初始化 OpenAI 提供者

        Args:
            api_key: OpenAI API 密钥
            model: OpenAI 模型名称
        """
        super().__init__(api_key, model)
        self.client = OpenAI(api_key=api_key)

    def analyze_image(
        self,
        image_path: Path,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        使用 OpenAI Vision API 分析图像

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
        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{media_type};base64,{image_data}"
                    }
                }
            ]
        })

        # 调用 API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=4096
        )

        return response.choices[0].message.content

    def text_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        OpenAI 文本生成

        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词（可选）
            temperature: 温度参数
            max_tokens: 最大 token 数

        Returns:
            AI 的文本响应
        """
        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content

    def structured_output(
        self,
        prompt: str,
        response_format: Dict[str, Any],
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        OpenAI 结构化输出（使用 JSON 模式）

        Args:
            prompt: 用户提示词
            response_format: 期望的响应格式（仅作为提示使用）
            system_prompt: 系统提示词（可选）

        Returns:
            结构化的 JSON 数据
        """
        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        # 在提示词中说明 JSON 格式要求
        json_prompt = f"""{prompt}

请以 JSON 格式返回结果。"""

        messages.append({
            "role": "user",
            "content": json_prompt
        })

        # 使用 JSON 模式
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.3  # 降低温度以提高准确性
        )

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"无法解析 OpenAI 返回的 JSON: {e}\n原始响应: {content}")
