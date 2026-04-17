from domain.common.exception import DomainError


class ReferralAwardError(DomainError): ...


class ReferralAwardPermissionDenied(ReferralAwardError): ...
