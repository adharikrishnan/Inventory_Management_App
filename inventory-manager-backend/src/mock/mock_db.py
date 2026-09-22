from schema.user import user

mock_users: list[user] = [
    user(
        id=1,
        username="johndoe",
        password_hash="$2b$12$eImiTXuWVxfM37uY4JANjO8e2s362194c502a.v2a0a202a0a202a",
        email="john.doe@example.com",
        first_name="John",
        last_name="Doe",
        disabled=False,
    ),
    user(
        id=2,
        username="janesmith",
        password_hash="$2b$12$k8B1L3s2J4k5L6m7N8o9P0q1R2s3T4u5V6w7X8y9Z0a1B2c3D4e5F",
        email="jane.smith@example.com",
        first_name="Jane",
        last_name="Smith",
        disabled=False,
    ),
    user(
        id=3,
        username="alexm",
        password_hash="$2b$12$Z0a1B2c3D4e5F6g7H8i9J0k1L2m3N4o5P6q7R8s9T0u1V2w3X4y5Z",
        email=None,  # Demonstrating optional field
        first_name="Alex",
        last_name="Morgan",
        disabled=True,
    ),
]
