AUTO_SHAPES = {
    # Databases
    "db": "cylinder",
    "database": "cylinder",
    "sql": "cylinder",
    "postgres": "cylinder",
    "mysql": "cylinder",
    "datalake": "cylinder",
    "datawarehouse": "cylinder",
    # Caches
    "cache": "box3d",
    "redis": "box3d",
    "memcached": "box3d",
    # Queues
    "queue": "parallelogram",
    "kafka": "parallelogram",
    "rabbitmq": "parallelogram",
    # Storage
    "bucket": "folder",
    "s3": "folder",
    "storage": "folder",
    # Components
    "api": "component",
    "service": "component",
    "server": "component",
    # Users
    "user": "ellipse",
    "customer": "ellipse",
    # Default
    "default": "box",
}


def get_auto_shape_for_node(node_name: str):
    normalized_node_name = node_name.lower()
    for key in AUTO_SHAPES:
        if key in normalized_node_name:
            return AUTO_SHAPES[key]
    return AUTO_SHAPES["default"]
