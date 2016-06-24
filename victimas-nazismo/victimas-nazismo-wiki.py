#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016 emijrp <emijrp@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pywikibot

def destraducirfecha(fecha):
    trad = fecha
    meses = {'enero':1, 'febrero':2, 'marzo':3, 'abril':4, 'mayo':5, 'junio':6, 'julio':7, 'agosto':8, 'septiembre':9, 'octubre':10, 'noviembre':11, 'diciembre':12}
    if len(fecha.split(' de ')) == 3:
        try:
            trad = '%s/%02d/%02d' % (int(fecha.split(' de ')[2]), int(meses[fecha.split(' de ')[1]]), int(fecha.split(' de ')[0]))
        except:
            trad = fecha
    
    return trad

def main():
    f = open('victimas-nazismo.csv', 'r')
    csv = unicode(f.read(), 'utf-8')
    f.close()
    
    rows = csv.split('\n')
    skip = u'Barbero Barbero, Gregorio'
    for row in rows:
        print row
        try:
            apellidosnombre, edad, procedencia, oficio, lugarfallecimiento, fechafallecimiento = row.split(';;;')
        except:
            continue
        
        if skip:
            if skip != apellidosnombre:
                continue
            else:
                skip = ''
        
        if ', ' in apellidosnombre:
            nombre = apellidosnombre.split(', ')[1]
            apellidos = apellidosnombre.split(', ')[0]
            nombreapellidos = u'%s %s' % (nombre, apellidos)
            if ' ' in apellidos:
                apellido1 = apellidos.split(' ')[0]
                apellido2 = ' '.join(apellidos.split(' ')[1:])
        elif ',' in apellidosnombre:
            nombre = apellidosnombre.split(',')[1]
            apellidos = apellidosnombre.split(',')[0]
            nombreapellidos = u'%s %s' % (nombre, apellidos)
            if ' ' in apellidos:
                apellido1 = apellidos.split(' ')[0]
                apellido2 = ' '.join(apellidos.split(' ')[1:])
        else:
            nombre = apellidosnombre
            nombreapellidos = apellidosnombre
            apellidos = ''
            apellido1 = ''
            apellido2 = ''
        
        if 'gusen' in lugarfallecimiento.lower():
            lugarfallecimiento = u'Campo de concentración de Gusen'
        else:
            continue
        
        if ' (' in procedencia:
            procedenciamuni = procedencia.split(' (')[0]
            procedenciaprov = procedencia.split(' (')[1].split(')')[0]
        else:
            procedenciaprov = ''
        
        if oficio == '-':
            oficio = u''
        
        fechafallecimiento2 = fechafallecimiento
        
        desc = u'Víctima española del nazismo'
        bio = u'%s era de [[%s]]%s. Cuando murió en el campo de concentración tenía %s años.<ref name="enrecuerdode" />' % (nombre, procedenciamuni, procedenciaprov and u', [[provincia de %s]]' % (procedenciaprov) or u'', edad)
        
        output = u"""{{Infobox Persona
|nombre=%s
|primer apellido=%s
|segundo apellido=%s
|sexo=Hombre
|lugar de nacimiento=%s
|fecha de nacimiento=
|lugar de fallecimiento=%s
|fecha de fallecimiento=%s
|ocupación=%s
|descripción=%s
|represión={{persona represaliada
|represión=Campo de concentración
|represor=Nazismo
|fecha=%s
|lugar=%s
|fallecimiento=Sí
}}
}}

'''%s''', [[Lista de víctimas españolas del nazismo|víctima española]] del [[nazismo]], fue deportado al [[%s]] en [[Austria]], donde murió el [[%s]].<ref name="enrecuerdode">{{en recuerdo de}}</ref>

== Biografía ==

%s

== Véase también ==
* [[Memoria histórica]]
* [[Nazismo]]
* [[Lista de víctimas españolas del nazismo]]

== Referencias ==
{{reflist}}

== Enlaces externos ==
{{enlaces externos}}

{{represión}}""" % (nombre, apellido1, apellido2, procedenciamuni, lugarfallecimiento, destraducirfecha(fechafallecimiento), oficio, desc, destraducirfecha(fechafallecimiento), lugarfallecimiento, nombreapellidos, lugarfallecimiento, fechafallecimiento, bio)
        #print output.encode('utf-8')
                
        page = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), nombreapellidos)
        if page.exists():
            print 'Ya existe', nombreapellidos.encode('utf-8')
            f = open('victimas-yaexiste.txt', 'a')
            output2 = u'%s\n%s' % (output, '-'*50)
            f.write(output2.encode('utf-8'))
            f.close()
        else:
            print output.encode('utf-8')
            page.text = output
            page.save(u'BOT - Creando página', botflag=False)
            
            redtext = u'#REDIRECT [[%s]]' % (nombreapellidos)
            red = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), apellidosnombre)
            red.text = redtext
            red.save(u'BOT - Creando redirección a [[%s]]' % (nombreapellidos), botflag=True)

if __name__ == '__main__':
    main()
