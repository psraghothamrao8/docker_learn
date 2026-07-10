import os

def get_message():
    # Looks for a secret key, defaults to "no-key" if missing
    secret = os.getenv("MY_SECRET", "no-key")
    return f"Hello! Secret is: {secret}"

if __name__ == "__main__":
    print(get_message())