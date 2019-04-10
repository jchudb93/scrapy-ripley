def obtener_sub_categoria_str(response_url):
    response_url = '-'.join(str(response_url.split('/')[5:]).split('-')[2:]).split('?')[0]
    return response_url

def obtener_tipo_producto(url, tipos_producto):
    
    assert tipos_producto is not None, 'Falta lista de tipo de productos'
    
    for item in tipos_producto:
        if item in url:
            item = item.replace('/','-')
            return item
    return ''