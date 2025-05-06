from django.http import FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rembg import remove
from PIL import Image
import urllib
from user_agents import parse

html = '''<!DOCTYPE html>
<html>
  <head>
    <title>Background Remover</title>
  </head>
  <body>
    <h1>Background Remover</h1>
    <form method="post" enctype="multipart/form-data">
      <div
        id="dropbox"
        style="
          border: 2px solid #b3b3b3;
          max-width: 100%;
          min-width: 100%;
          max-height: 200px;
          min-height: 200px;
          padding: 5px;
        "
      >
        <p>Drop your file here or</p>
        <input type="file" id="image" name="image" /><br />
        <input type="text" id="url" name="url" hidden /><br />
      </div>
      <input type="submit" id="submit" value="Submit" hidden />
    </form>

    <script>
      var dropbox = document.getElementById("dropbox");
      var submit = document.getElementById("submit");
      var filefield = document.getElementById("image");

      dropbox.addEventListener("dragenter", noopHandler, false);
      dropbox.addEventListener("dragexit", noopHandler, false);
      dropbox.addEventListener("dragover", noopHandler, false);
      dropbox.addEventListener("drop", drop, false);
      filefield.addEventListener(
        "change",
        () => {
          submit.click();
        },
        false
      );

      function noopHandler(evt) {
        evt.stopPropagation();
        evt.preventDefault();
      }

      function drop(evt) {
        clearFileInput(filefield)
        evt.stopPropagation();
        evt.preventDefault();
        var imageUrl = evt.dataTransfer.getData("url");
        if (imageUrl) {
          document.getElementById("url").value = imageUrl;
          submit.click();
          return;
        }
        var file = evt.dataTransfer.files;
        filefield.files = file;
        submit.click();
      }

      function clearFileInput(ctrl) {
        try {
            ctrl.value = null;
        } catch(ex) { }
        if (ctrl.value) {
            ctrl.parentNode.replaceChild(ctrl.cloneNode(true), ctrl);
        }
      }
    </script>
  </body>
</html>
'''


@csrf_exempt
def removebg(request):
    if request.method == 'GET':
        return HttpResponse(html)
    if request.method == 'POST':
        try:
            image = request.FILES.get("image")
            name = "file.png"
            if image:
                inp = Image.open(image)
                name = image.name + '.png'
            else:
                url = request.POST.get("url")
                print(f'attempting to open {url} as image')
                name = url[url.rfind('/'):] + '.png'
                inp = Image.open(urllib.request.urlopen(url))
            output = remove(inp)
            output.save("temp.png")
            user_agent = parse(request.headers['user-agent'])
            # firefox and mobile don't preserve the modified image for subsequent save as operation so save immediately
            if 'Firefox' in user_agent.browser.family or user_agent.is_mobile:
                return FileResponse(open("temp.png", "rb"), as_attachment=True, filename=name)
            else:
                return FileResponse(open("temp.png", "rb"), filename=name)
        except:
            return HttpResponse(html)
