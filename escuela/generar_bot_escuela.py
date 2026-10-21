"""Genera apps_script/bot/BotEscuela.html a partir de escuela/programa.json.
Uso: python3 escuela/generar_bot_escuela.py"""
import json, os
raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
programa = json.load(open(os.path.join(raiz, 'escuela', 'programa.json'), encoding='utf-8'))
# Para la sala alcanza con cursos, lecciones y preguntas (el resto lo usa el panel).
liviano = {
    'version': programa['version'],
    'cursos': [{
        'id': c['id'], 'titulo': c['titulo'], 'para': c['para'],
        'lecciones': [{'id': l['id'], 'titulo': l['titulo'], 'preguntas': l['preguntas']} for l in c['lecciones']],
    } for c in programa['cursos']],
}
salida = os.path.join(raiz, 'apps_script', 'bot', 'BotEscuela.html')
with open(salida, 'w', encoding='utf-8') as f:
    f.write('<script>\n// Banco de preguntas de la Escuela de Mercado Libre Argentina (generado desde escuela/programa.json).\n'
            '// No editar a mano: cambiá programa.json y corré escuela/generar_bot_escuela.py.\n'
            'const ESCUELA = ' + json.dumps(liviano, ensure_ascii=False) + ';\n</script>\n')
print('BotEscuela.html', os.path.getsize(salida) // 1024, 'KB')
