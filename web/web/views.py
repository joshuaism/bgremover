from django.http import FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rembg import remove
from PIL import Image


@csrf_exempt
def removebg(request):
    if request.method == 'GET':
        return HttpResponse(
            '''<h1>Background Remover</h1>
                <form method="post" enctype="multipart/form-data">
                <input type="file" id="image" name="image"><br>
                <input type="submit" value="Submit">
                </form> ''')
    if request.method == 'POST':
        try:
            image = request.FILES.get("image")
            inp = Image.open(image)
            output = remove(inp)
            output.save("temp.png")
            return FileResponse(open("temp.png", "rb"), filename=image.name)
        except:
            return HttpResponse(
                '''<h1>Background Remover</h1>
                <form method="post" enctype="multipart/form-data">
                <input type="file" id="image" name="image"><br>
                <input type="submit" value="Submit">
                </form> 
                <p>not an image file</p>''')
