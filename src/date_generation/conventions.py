from pydantic.dataclasses import dataclass


@dataclass
class GeneralConventions:
    frequency_yearly: str = "yearly"
    frequency_monthly: str = "monthly"
