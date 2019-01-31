'''
Simple example showing potential of  pushing content pprogrammatically 
from DNA analysis pipelines into an end-user (scientist's ELN)

This example just takes the most trivial example from `dna_features_viewer` docs
 and sends output image to an new RSpace document.

 You could also send raw sequence files as well.
Usage plot.py <RSPACE_URL> <API_KEY>

'''
from dna_features_viewer import GraphicFeature, GraphicRecord
import rspace_client
features=[
            GraphicFeature(start=0, end=20, strand=+1, color="#ffd700",
                                   label="Small feature"),
                GraphicFeature(start=20, end=500, strand=+1, color="#ffcccc",
                                       label="Gene 1 with a very long name"),
                    GraphicFeature(start=400, end=700, strand=-1, color="#cffccc",
                                           label="Gene 2"),
                        GraphicFeature(start=600, end=900, strand=+1, color="#ccccff",
                                               label="Gene 3")
                        ]
record = GraphicRecord(sequence_length=1000, features=features)
a, _=record.plot(figure_width=5)
a.figure.savefig("out.png")
client = rspace_client.utils.createClient()
# Creating a new Basic document in Api Inbox folder
new_document = client.create_document(name='Python API Example Basic Document', tags=['Python', 'API', 'example'],
                               fields=[{'content': 'Some example text'}])
print('New document was successfully created with global ID {}'.format(new_document['globalId']))

# Uploading a file to the gallery
with open('out.png', 'rb') as f:
    new_file = client.upload_file(f, caption='some caption')
    print('File "{}" was uploaded as {} ({})'.format(f.name, new_file['name'], new_file['globalId']))

    # Editing the document to link to the uploaded file
    updated_document = client.update_document(new_document['id'], fields=[{
                    'content': 'Some example text. Link to the uploaded file: <fileId={}>'.format(new_file['id'])
                    }])
    print('Document has been updated to link to the uploaded file.')
