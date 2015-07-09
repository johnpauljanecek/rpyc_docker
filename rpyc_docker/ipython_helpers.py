def dicts_to_html(dicts,keys = None):
    from IPython.display import HTML
    if not keys :
        keys = dicts[0].keys()
    rows = ["<table>"]
    header = ["<tr>"]
    for key in keys :
        header.append("<th>"+key+"</th>")
    header.append("</tr>")
    rows.append("".join(header))

    for d in dicts :
        row = ["<tr>"]
        for key in keys :
            row.append("<td>" + str(d[key]) + "</td>")
        row.append("</tr>")
        rows.append("".join(row))
    
    rows.append("</table>")
    return HTML("".join(rows))

def dict_to_html(_dict,keys = None,ignore_keys = []):
    from IPython.display import HTML
    
    if not keys :
        keys = _dict.keys()
    
    for k in ignore_keys :
        keys.remove(k)

    rows = ["<table>"]
    header = ["<tr>"]
    for col in ["name","value"] :
        header.append("<th>"+col+"</th>")
    header.append("</tr>")
    rows.append("".join(header))
    
    for key in keys:
        rows.append("<tr><td>%s</td><td>%s</td></tr>" 
                    % (key,str(_dict[key])))

    rows.append("</table>")
    return HTML("".join(rows))

def obj_to_html(obj):
    return  dict_to_html(obj.__dict__)    

def objs_to_html(objs):
    return dicts_to_html(map(lambda obj: obj.__dict__,objs))
