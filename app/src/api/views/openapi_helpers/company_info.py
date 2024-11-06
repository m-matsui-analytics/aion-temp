from drf_spectacular.utils import OpenApiParameter, OpenApiTypes

company_info_parameters = [
    OpenApiParameter(
        name="foundation_date",
        type=OpenApiTypes.DATE,
        location=OpenApiParameter.QUERY,
        required=False,
        description="設立日"
    ),
    OpenApiParameter(
        name="capital",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
        required=False,
        description="資本金（万円）"
    ),
    OpenApiParameter(
        name="post_code",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
        required=False,
        description="郵便番号(7桁、ハイフンなし)"
    ),
    OpenApiParameter(
        name="address_prefecture_id",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
        required=False,
        description="所在地(都道府県)のID"
    ),
    OpenApiParameter(
        name="address_other",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        required=False,
        description="所在地(県以下)"
    ),
    OpenApiParameter(
        name="ceo_name",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        required=False,
        description="代表者名"
    ),
    OpenApiParameter(
        name="employee_size",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
        required=False,
        description="従業員数"
    ),
    OpenApiParameter(
        name="business_description",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        required=False,
        description="事業内容"
    ),
    OpenApiParameter(
        name="industry",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
        required=False,
        description="業種"
    ),
    OpenApiParameter(
        name="revenue",
        type=OpenApiTypes.INT,
        location=OpenApiParameter.QUERY,
        required=False,
        description="売上高（万円）"
    ),
    OpenApiParameter(
        name="mission",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        required=False,
        description="ミッション"
    ),
    OpenApiParameter(
        name="vision",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        required=False,
        description="ビジョン"
    ),
    OpenApiParameter(
        name="value",
        type=OpenApiTypes.STR,
        location=OpenApiParameter.QUERY,
        required=False,
        description="バリュー"
    ),
]