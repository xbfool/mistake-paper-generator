"""
AI 提供者抽象层
支持 Claude 和 OpenAI 两种 AI 模型
"""
import os
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pathlib import Path
import base64


class AIProvider(ABC):
    """AI 提供者抽象基类"""

    def __init__(self, api_key: str = None, model: str = None):
        """
        初始化 AI 提供者

        Args:
            api_key: API 密钥
            model: 模型名称
        """
        self.api_key = api_key
        self.model = model

    @abstractmethod
    def analyze_image(
        self,
        image_path: Path,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        分析图像

        Args:
            image_path: 图像路径
            prompt: 用户提示词
            system_prompt: 系统提示词（可选）

        Returns:
            AI 的文本响应
        """
        pass

    @abstractmethod
    def text_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        文本生成

        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词（可选）
            temperature: 温度参数
            max_tokens: 最大 token 数

        Returns:
            AI 的文本响应
        """
        pass

    @abstractmethod
    def structured_output(
        self,
        prompt: str,
        response_format: Dict[str, Any],
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        结构化输出（JSON 格式）

        Args:
            prompt: 用户提示词
            response_format: 期望的响应格式
            system_prompt: 系统提示词（可选）

        Returns:
            结构化的 JSON 数据
        """
        pass

    @staticmethod
    def encode_image(image_path: Path) -> str:
        """
        将图片编码为 base64

        Args:
            image_path: 图片路径

        Returns:
            base64 编码的图片字符串
        """
        with open(image_path, "rb") as image_file:
            return base64.standard_b64encode(image_file.read()).decode("utf-8")

    @staticmethod
    def get_image_mime_type(image_path: Path) -> str:
        """
        获取图片的 MIME 类型

        Args:
            image_path: 图片路径

        Returns:
            MIME 类型字符串
        """
        suffix = image_path.suffix.lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        return mime_types.get(suffix, 'image/jpeg')


def get_ai_provider(provider_name: Optional[str] = None) -> AIProvider:
    """
    获取 AI 提供者实例

    Args:
        provider_name: 提供者名称（'claude' 或 'openai'），如果不指定则从环境变量读取

    Returns:
        AI 提供者实例

    Raises:
        ValueError: 如果提供者名称无效或 API 密钥未配置
    """
    from .claude_provider import ClaudeProvider
    from .openai_provider import OpenAIProvider

    # 确定使用哪个提供者
    provider = provider_name or os.getenv('DEFAULT_AI_PROVIDER', 'claude')
    provider = provider.lower()

    if provider == 'claude':
        # 支持新旧两种环境变量名
        api_key = os.getenv('CLAUDE_API_KEY') or os.getenv('ANTHROPIC_API_KEY')
        model = os.getenv('CLAUDE_MODEL', 'claude-sonnet-4.5-20250929')

        if not api_key:
            raise ValueError(
                "未找到 Claude API 密钥。请在 .env 文件中配置 CLAUDE_API_KEY 或 ANTHROPIC_API_KEY"
            )

        return ClaudeProvider(api_key=api_key, model=model)

    elif provider == 'openai':
        api_key = os.getenv('OPENAI_API_KEY')
        model = os.getenv('OPENAI_MODEL', 'gpt-4o')

        if not api_key:
            raise ValueError(
                "未找到 OpenAI API 密钥。请在 .env 文件中配置 OPENAI_API_KEY"
            )

        return OpenAIProvider(api_key=api_key, model=model)

    else:
        raise ValueError(
            f"不支持的 AI 提供者: {provider}。请使用 'claude' 或 'openai'"
        )
