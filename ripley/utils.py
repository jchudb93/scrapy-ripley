def obtener_sub_categoria_str(response_url):
    response_url = '-'.join(str(response_url.split('/')[5:]).split('-')[2:]).split('?')[0]
    return response_url