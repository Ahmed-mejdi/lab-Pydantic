from pydantic import BaseModel, EmailStr, field_validator

# Step 3: Create a basic Pydantic model
class User(BaseModel):
    name: str
    email: EmailStr
    account_id: int
    
    # Step 4: Add custom field validation
    @field_validator("account_id")
    def validate_account_id(cls, value):
        if value <= 0:
            raise ValueError(f"account_id must be positive: {value}")
        return value

# Step 5: Create instances in different ways
# Method 1: Direct initialization
def create_user_direct():
    try:
        user = User(
            name="Salah",
            email="salah@gmail.com",
            account_id=12345
        )
        print("\nUser created successfully:")
        print(f"Name: {user.name}")
        print(f"Email: {user.email}")
        print(f"Account ID: {user.account_id}")
        return user
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

# Method 2: From dictionary
def create_user_from_dict():
    try:
        user_data = {
            'name': 'Ali',
            'email': 'ali@gmail.com',
            'account_id': 5678
        }
        user = User(**user_data)
        print("\nUser created from dictionary:")
        print(f"Name: {user.name}")
        print(f"Email: {user.email}")
        print(f"Account ID: {user.account_id}")
        return user
    except Exception as e:
        print(f"Error creating user from dict: {e}")
        return None

# Step 6: Demonstrate validation errors
def show_validation_errors():
    print("\nDemonstrating validation errors:")
    
    # Invalid email
    try:
        User(name="John", email="not-an-email", account_id=100)
    except Exception as e:
        print(f"Invalid email error: {e}")
    
    # Invalid account_id (negative)
    try:
        User(name="John", email="john@example.com", account_id=-10)
    except Exception as e:
        print(f"Invalid account ID error: {e}")
    
    # Type error (string instead of int)
    try:
        User(name="John", email="john@example.com", account_id="abc")
    except Exception as e:
        print(f"Type error: {e}")

# Step 7: JSON serialization and deserialization
def demonstrate_serialization(user):
    if not user:
        return
        
    print("\nJSON Serialization:")
    
    # Convert to JSON string
    user_json = user.model_dump_json()
    print(f"JSON string: {user_json}")
    
    # Convert to dictionary
    user_dict = user.model_dump()
    print(f"Python dict: {user_dict}")
    
    # Parse from JSON string
    try:
        new_user = User.model_validate_json(user_json)
        print(f"Parsed from JSON: {new_user.name}, {new_user.email}")
    except Exception as e:
        print(f"Error parsing JSON: {e}")

# Step 8: Create more complex models
class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class DetailedUser(User):
    age: int
    is_active: bool = True  # Default value
    addresses: list[Address] = []  # List of Address objects
    
    @field_validator("age")
    def validate_age(cls, value):
        if value < 18:
            raise ValueError(f"User must be at least 18 years old, got {value}")
        return value

def demonstrate_nested_models():
    print("\nNested Models:")
    try:
        # Create a user with addresses
        user = DetailedUser(
            name="Sarah",
            email="sarah@example.com",
            account_id=9012,
            age=25,
            addresses=[
                Address(street="123 Main St", city="New York", country="USA", postal_code="10001"),
                Address(street="456 Park Ave", city="Boston", country="USA", postal_code="02108")
            ]
        )
        
        print(f"User: {user.name}, Age: {user.age}")
        print(f"Number of addresses: {len(user.addresses)}")
        for i, addr in enumerate(user.addresses):
            print(f"Address {i+1}: {addr.street}, {addr.city}")
            
        # Serialize nested model
        print("\nSerialized nested model:")
        print(user.model_dump_json())
        
    except Exception as e:
        print(f"Error with nested models: {e}")

# Main execution
if __name__ == "__main__":
    print("Pydantic Tutorial Implementation\n")
    
    user1 = create_user_direct()
    user2 = create_user_from_dict()
    show_validation_errors()
    demonstrate_serialization(user1)
    demonstrate_nested_models()