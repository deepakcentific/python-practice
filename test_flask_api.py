from flask_api import app

def test_home1():
	print("Testing home endpoint... from test_home1()")

	# Using with statement to ensure the test client is properly closed after the test
	"""
	What is with in Python? 
	The with statement is used for objects that need setup and cleanup.
	
	This means:
		Create a test client.
		Enter a special context.
		Run the code inside the block.
		Automatically clean up resources when the block ends.
	"""
	with app.test_client() as client:
		response = client.get('/')
		assert response.status_code == 200
		assert response.get_json() == {"message": "Sample Flask API endpoint!"}

def test_home2():
    print("Testing home endpoint... from test_home2()")

    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {"message": "Sample Flask API endpoint!"}		