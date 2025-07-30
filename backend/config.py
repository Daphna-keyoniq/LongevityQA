from pathlib import Path
from pydantic import BaseModel, Field, field_validator
import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any


class LoggingConfig(BaseModel):
    """Configuration for logging

    Attributes:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format: Log format (json or text)
        log_to_file: Whether to log to file
        log_to_console: Whether to log to console
    """

    log_level: str = Field(default="INFO")
    log_format: str = Field(default="json")
    log_to_file: bool = Field(default=True)
    log_to_console: bool = Field(default=True)

    @field_validator("log_level")
    @classmethod
    def validate_level(cls, v):
        """Validate logging level.

        Note: Using cls instead of self because this is a class method in Pydantic.
        """
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Logging level must be one of {valid_levels}")
        return v.upper()

    @field_validator("log_format")
    @classmethod
    def validate_format(cls, v):
        """Validate log format."""
        valid_formats = ["json", "text"]
        if v.lower() not in valid_formats:
            raise ValueError(f"Log format must be one of {valid_formats}")
        return v.lower()


class Paths(BaseModel):
    """Configuration for all file system paths

    Attributes:
        base_dir: Base directory for the application
        input_dir: Directory for input data
        output_dir: Directory for output data
        logs_dir: Directory for logs
        temp_dir: Directory for temporary files
    """

    base_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent)
    # relative path
    input_dir: Path = Field(default_factory=lambda: Path("input_data"))
    output_dir: Path = Field(default_factory=lambda: Path("output_data"))
    logs_dir: Path = Field(default_factory=lambda: Path("logs"))
    temp_dir: Path = Field(default_factory=lambda: Path("input_data/temp"))
    knowledge_dir: Path = Field(
        default_factory=lambda: Path("backend/knowledge")
    )

    def __init__(self, **data):
        super().__init__(**data)
        # Create necessary directories
        for path in [
            self.input_dir,
            self.output_dir,
            self.logs_dir,
            self.temp_dir,
        ]:
            path.mkdir(parents=True, exist_ok=True)

    @property
    def full_input_dir(self) -> Path:
        """Get full path to input directory."""
        return self.base_dir / self.input_dir

    @property
    def full_output_dir(self) -> Path:
        """Get full path to output directory."""
        return self.base_dir / self.output_dir

    @property
    def full_logs_dir(self) -> Path:
        """Get full path to logs directory."""
        return self.base_dir / self.logs_dir

    @property
    def full_temp_dir(self) -> Path:
        """Get full path to temporary directory."""
        return self.base_dir / self.temp_dir

    @property
    def full_knowledge_dir(self) -> Path:
        """Get full path to knowledge directory."""
        return self.base_dir / self.knowledge_dir


class LLMConfig(BaseModel):
    """Configuration for LLM-related settings

    Attributes:
        model: LLM model name
        api_key: API key for the LLM service
        temperature: Temperature for generation
        max_tokens: Maximum tokens for generation
    """

    model: str = Field(default="gpt-4")
    api_key: str
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=2000, gt=0)

    @field_validator("api_key")
    @classmethod
    def validate_api_key(cls, v):
        """Validate API key is not empty.

        Note: Using cls instead of self because this is a class method in Pydantic.
        """
        if not v:
            raise ValueError("API key cannot be empty")
        return v


class AuthConfig(BaseModel):
    """Configuration for authentication

    Attributes:
        username: Username for authentication
        password: Password for authentication
    """

    SECRET_KEY: str

    @field_validator("username", "password", check_fields=False)
    @classmethod
    def validate_credentials(cls, v):
        """Validate credentials are not empty."""
        assert v is not None, "SECRET_KEY is not set"
        return v


class DatabaseConfig(BaseModel):
    """Configuration for database

    Attributes:
        db_config: Database configuration dictionary
        backup_enabled: Whether backups are enabled
        backup_interval_hours: Backup interval in hours
        schema_name: Optional schema name for database operations
    """

    db_config: Dict[str, Any] = Field(default_factory=dict)
    backup_enabled: bool = Field(default=True)
    backup_interval_hours: int = Field(default=24, gt=0)
    schema_name: Optional[str] = Field(default=None)


class DevConfig(BaseModel):
    """Login for the frontend

    Attributes:
        username: Development username
        password: Development password
        email: Development email
    """

    username: str
    password: str
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        """Validate email format."""
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v


class StorageConfig(BaseModel):
    """Configuration for Azure Blob Storage

    Attributes:
        connection_string: Azure Blob Storage connection string
        account_name: Azure Blob Storage account name
        account_key: Azure Blob Storage account key
        container_name: Azure Blob Storage container name
    """

    connection_string: str
    account_name: str
    account_key: str
    container_name: str = Field(default="lqa-files")

    @field_validator("connection_string", "account_name", "account_key")
    @classmethod
    def validate_required_fields(cls, v):
        """Validate required fields are not empty."""
        assert v is not None, "Required Azure Storage configuration is missing"
        return v


class Config:
    """Main configuration class that combines all configuration aspects

    This class loads and validates all configuration from environment variables
    and provides access to all configuration sections.
    """

    # Configuration sections
    paths: Paths = Field(default_factory=Paths)
    llm: LLMConfig
    auth: AuthConfig
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    database: DatabaseConfig
    dev: DevConfig
    storage: StorageConfig

    @classmethod
    def load_configuration(cls, type: str = "test") -> "type[Config]":
        """Load and validate all configuration from environment variables.

        Returns:
            Config: A validated configuration instance
        """
        # Load environment variables
        # define which .env file to be used
        if type == "test":
            env_file = ".env.test"
        elif type == "prod":
            env_file = ".env.prod"
        else:
            raise ValueError(f"Invalid environment type: {type}")
        env_file_encoding = "utf-8"  # default encoding
        load_dotenv(dotenv_path=env_file, override=True, encoding=env_file_encoding)

        # Configure postgres database
        db_config = {
            "dbname": os.getenv("POSTGRES_DB", "longevity_qa"),
            "user": os.getenv("POSTGRES_USER", "postgres"),
            "password": os.getenv("POSTGRES_PASSWORD", ""),
            "host": os.getenv("POSTGRES_HOST", "localhost"),
            "port": os.getenv("POSTGRES_PORT", "5432"),
        }

        # Get schema from environment
        schema = os.getenv("DB_SCHEMA", None)

        # Create config instance
        cls.llm = LLMConfig(
            api_key=os.getenv("OPENAI_API_KEY", ""), model=os.getenv("MODEL", "gpt-4o")
        )
        cls.auth = AuthConfig(
            SECRET_KEY=os.getenv("SECRET_KEY", ""),
        )
        cls.database = DatabaseConfig(db_config=db_config, schema_name=schema)
        cls.paths = Paths()
        cls.dev = DevConfig(
            username=os.getenv("DEV_USERNAME", "devuser"),
            password=os.getenv("DEV_PASSWORD", "supersecurepassword123"),
            email=os.getenv("DEV_EMAIL", "devuser@keyoniq.ai"),
        )
        cls.storage = StorageConfig(
            connection_string=os.getenv("AZURE_STORAGE_CONNECTION_STRING", ""),
            account_name=os.getenv("AZURE_STORAGE_ACCOUNT_NAME", ""),
            account_key=os.getenv("AZURE_STORAGE_ACCOUNT_KEY", ""),
            container_name=os.getenv("AZURE_STORAGE_CONTAINER_NAME", "lqa-files"),
        )

        return cls
