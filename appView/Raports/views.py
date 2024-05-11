import json
from django.shortcuts import render
from Raports.models import Set, Pmta, Mint
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import subprocess

def index(request):
    sets = Pmta.objects.order_by('set_name')
    serialized_sets = []

    for obj in sets:
        serialized_sets.append({
            'set_name': str(obj.set_name),
            'date': obj.date.strftime('%Y-%m-%d'),  # Convert date to string
            'hour': obj.hour,
            'number_send': obj.number_send,
            'ip': obj.ip,
            'id_mint': obj.id_mint
        })

    serialized_sets_json = json.dumps(serialized_sets)
    return render(request, 'index.html', {'sets': serialized_sets_json})


def vmtas(request):
    return render(request,'vmtas.html')

def send_test(request):
    return render(request,'send_test.html')

@require_http_methods(["GET"])
def getVmtas(request):
    # Directory to list files from
    remote_directory = '/etc/pmta/projects'

    try:

        # Execute command to list files in the directory
        command = ['ssh', '-p', '24', 'root@89.44.100.51', f'ls {remote_directory}']
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Split the output into lines to get file names
        file_names = result.stdout.splitlines()
        # Convert file names to array of objects
        file_objects = [{"set": file_name} for file_name in file_names]

    except subprocess.CalledProcessError as e:
        # Handle command execution errors
        print(f"Error executing command: {e}")
        return JsonResponse({'error': str(e)}, status=500)

    except Exception as e:
        # Handle any other exceptions
        print(f"Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    # Return the array of objects directly as JSON response
    return JsonResponse(file_objects, safe=False)

@require_http_methods(["GET"])
def getVmtaLog(request):
    # Directory to search for files
    remote_directory = '/etc/pmta/projects'

    # Get the file name from the request parameters
    file_name = request.GET.get('name')
    if not file_name:
        return JsonResponse({'error': 'File name parameter is missing'}, status=400)

    try:

        # If the file exists, execute command to read its content
        command = ['ssh', '-p', '24', 'root@89.44.100.51', f'cat {remote_directory}/{file_name}']
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Get the content of the file
        file_content = result.stdout
        return JsonResponse({'file_content': file_content})

    except subprocess.CalledProcessError as e:
        # Handle command execution errors (e.g., file not found)
        print(f"Error executing command: {e}")
        return JsonResponse({'error': f'File not found: {file_name}'}, status=404)

    except Exception as e:
        # Handle any other exceptions
        print(f"Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    
    
@require_http_methods(["GET"])
def saveVmtaLog(request):
    remote_host = '89.44.100.51'
    remote_port = 24
    remote_username = 'root'
    remote_directory = '/etc/pmta/projects'
    file_name = request.GET.get('name')
    file_content = request.GET.get('file')
    try:
        # Construct the SSH command
        command = [
            'ssh', 
            '-p', str(remote_port), 
            f'{remote_username}@{remote_host}',
            f'echo "{file_content}" > {remote_directory}/{file_name}'
        ]
        
        # Execute the SSH command
        subprocess.run(command, check=True)
        
        return JsonResponse({'success': True})
    except Exception as e:
        # Handle exceptions
        return JsonResponse({'error': str(e)}, status=500)