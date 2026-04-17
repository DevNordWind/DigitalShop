from domain.common.exception import DomainError


class ReferralPolicyError(DomainError): ...


class ReferralPolicyNotCreated(ReferralPolicyError): ...


class ReferralPolicyPermissionDenied(ReferralPolicyError): ...
