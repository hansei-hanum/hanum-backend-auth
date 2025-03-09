from services.user import UserVerification


department_map = {
    "CLOUD_SECURITY": "클라우드보안과",
    "NETWORK_SECURITY": "네트워크보안과",
    "HACKING_SECURITY": "해킹보안과",
    "METAVERSE_GAME": "메타버스게임과",
    "INTELLIGENT_SOFTWARE": "지능형소프트웨어과",
    "GAME": "게임과",
}


def get_userinfo_string(verification: UserVerification | None) -> str:
    if verification is None:
        return "미인증 사용자"
    if verification.type == "TEACHER":
        return "한세사이버보안고등학교 교직원"
    elif verification.type == "GRADUATED":
        return f"{verification.graduated_at}년도 졸업생"
    else:
        return f"{department_map[verification.department]} {verification.grade}학년 {verification.classroom}반 재학생"
