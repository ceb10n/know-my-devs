from pydantic import BaseModel


class WebhookHeaders(BaseModel):

    x_github_hook_id: str
    x_github_event: str
    x_github_delivery: str
    x_hub_signature: str
    x_hub_signature_256: str
    user_agent: str
    x_github_hook_installation_target_type: str
    x_github_hook_installation_target_id: str
