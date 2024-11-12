from django.db import models
import csv

# Create your models here.
class Voter(models.Model):
    voter_id = models.CharField(max_length=12, primary_key=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.CharField(max_length=10)
    
    # Participation fields
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    
    # Voter score
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


def load_data():
    '''Load the data records from a CSV file, create Django model instances.'''

    # delete all records:
    Voter.objects.all().delete()

    # open the file for reading one line at a time
    # Define the path to the CSV file
    filename = 'voter_analytics/data/newton_voters.csv'  # Adjust the path as necessary
    f = open(filename) # open the file for reading
    headers = f.readline() # discard the first line containing headers


    for line in f:
        try:
            # Split the line into fields
            fields = line.strip().split(',')

            # Create a new Voter instance
            voter = Voter(
                voter_id=fields[0].strip(),  # Assuming Voter ID Number is the first column
                last_name=fields[1],
                first_name=fields[2],
                street_number=fields[3].strip(),
                street_name=fields[4],
                apartment_number=fields[5] if fields[5] else None,  # Handle empty fields
                zip_code=fields[6].strip(),
                date_of_birth=fields[7],
                date_of_registration=fields[8],
                party_affiliation=fields[9].strip(),
                precinct_number=fields[10],
                v20state=fields[11].strip().lower() == 'true',
                v21town=fields[12].strip().lower() == 'true',
                v21primary=fields[13].strip().lower() == 'true',
                v22general=fields[14].strip().lower() == 'true',
                v23town=fields[15].strip().lower() == 'true',
                voter_score=int(fields[16])
            )

            # Save the instance to the database
            voter.save()
            #print(f'Created voter: {voter}')

        except Exception as e:
            print(f"Exception occurred with fields: {fields}. Error: {e}")

    # After the loop
    print("Data loading complete.")