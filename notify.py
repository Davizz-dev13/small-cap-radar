#!/usr/bin/env python3
"""Notify only newly crossing 6/7, never on initial baseline."""
import json, os, sys, urllib.parse, urllib.request
from pathlib import Path
root=Path(__file__).resolve().parent
scan=json.loads((root/'docs'/'scan.json').read_text())
now={r['ticker']:r['score'] for r in scan['results'] if 'score' in r and 'error' not in r}
statepath=root/'alert_state.json'
prior=json.loads(statepath.read_text()) if statepath.exists() else None
crossed=[t for t,score in now.items() if score>=6 and prior is not None and prior.get(t,0)<6]
if crossed:
    token=os.getenv('TELEGRAM_BOT_TOKEN'); chat=os.getenv('TELEGRAM_CHAT_ID')
    if not token or not chat:raise RuntimeError('Telegram credentials missing; alert state NOT advanced')
    text='Radar precatalizador: cruce nuevo a 6/7 o más: '+', '.join(f'{t} ({now[t]}/7)' for t in crossed)+'. Universo semilla curado, no barrido global. 6/7 NO es señal de compra; revisar dilución, evento y fuentes. https://davizz-dev13.github.io/small-cap-radar/'
    data=urllib.parse.urlencode({'chat_id':chat,'text':text}).encode()
    request=urllib.request.Request('https://api.telegram.org/bot'+token+'/sendMessage',data=data,method='POST')
    with urllib.request.urlopen(request,timeout=20) as res:
        reply=json.loads(res.read())
        if not reply.get('ok'):raise RuntimeError('Telegram did not confirm message')
statepath.write_text(json.dumps(now,indent=2,sort_keys=True)+'\n')
print('Established baseline' if prior is None else 'Crossings: '+(', '.join(crossed) or 'none'))
