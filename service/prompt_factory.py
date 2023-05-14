from service.prompt_container import PromptContainer


class PromptFactory:
    def __init__(self, is_cloud_runtime=False):
        self.prompts = {
            "regular": PromptContainer(is_cloud_runtime).intro_prompt,
            "wallet_connect": PromptContainer(is_cloud_runtime).wallet_connect_prompt,
        }

    def get_prompt(self, prompt_name: str, **kwargs) -> str:
        """
        Get a prompt by name
        """
        return self.prompts[prompt_name].format(**kwargs)
