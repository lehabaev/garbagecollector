# GarbageCollector

##Need install
easy_install xmpppy
easy_install dnspython

*GarbageCollector* - тулза для определения, кому выпадет жребий выбрасывать мусор в офисе :)

Работает так:

1. Вначале через админку в базу вносятся данные о тех, кто работает в офисе: имя, фамилия и список MAC-адресов всех принадлежащих этому человеку сетевых устройств (ноутбуки, телефоны, планшеты и т.д.).

1. При запуске тулза определяет, какие устройства сейчас доступны в сети (с помощью nmap), получает их MAC-адреса и таким образом определяет, кто сейчас присутствует в офисе.

1. Далее случайным образом выбирается, кто будет выносить мусор, причем только среди тех, кто сейчас присутствует в офисе (чьи устройства активны)

###Лицензия

Copyright (c) 2012, Ilya Stepanov

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
