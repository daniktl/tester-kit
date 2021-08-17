import os


class Config:

    use_proxy = False
    proxy_host: str = os.getenv("PROXY_HOST")
    proxy_port: int = os.getenv("PROXY_PORT")
    proxy_username: str = os.getenv("PROXY_USERNAME")
    proxy_password: str = os.getenv("PROXY_PASSWORD")
