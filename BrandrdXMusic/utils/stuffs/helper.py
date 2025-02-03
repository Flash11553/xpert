# helper for strings

class Helper:
    HELP_M = """KATEQORİYANIZI SEÇİN  
Hansı mövzuda köməyə ehtiyacınız varsa, dəstək söhbətində suallarınızı verin.

Bütün əmrlər belə istifadə oluna bilər: /
"""

    HELP_ChatGPT = """ChatGPT

ChatGPT ƏMRLƏRİ:

/effect (/ask) ➠ Süni Zəka modelinə suallarınızı verib cavab alın.
"""

    HELP_Reel = """Relslər

Reelslər ƏMRLƏRİ:

/ig [URL] ➠ Instagram videolarını yükləyin. Komandanın ardından Instagram URL-ni qeyd edin.
/instagram [URL] ➠ Instagram videolarını yükləyin. URL-ni qeyd edin.
/reel [URL] ➠ Instagram videolarını yükləyin. URL-ni qeyd edin.
"""

    HELP_TagAll = """Tag-etmə

Tag-etmə ƏMRLƏRİ:

✿ Çatda tag seçin ✿

๏ /utag (/all)➛ Qrupda istifadəçiləri tağ edər 
Dayandırmaq üçün: /cancel

๏ /srtag ➛ Sabahınız xeyir tagı  
Tagı dayandırmaq üçün: /srstop

๏ /grtag ➛ Gecəniz xeyir tagı  
Tagı dayandırmaq üçün: /grstop

๏ /tagall ➛ Təsadüfi mesaj tagı  
Dayandırmaq üçün: /tagoff /tagstop"""

    HELP_Info = """İnfo

İnfo ƏMRLƏRİ:

/id : Mövcud qrupun ID-sini alın. Mesaja cavab olaraq istifadə edildikdə həmin istifadəçinin ID-sini göstərir.  
/info : İstifadəçi haqqında məlumat alın.
"""

    HELP_History = """İstifadəçi Tarixi

İstifadəçi Tarixi ƏMRLƏRİ:

Qrup idarəetmə əmrləri:

⦿ /sm  
Təsadüfi bir istifadəçinin mesaj tarixçəsindən məlumat toplayır.

İstifadə qaydası:  
⦿ /sm [istifadəçi adı/ID/cavab ver]
Detallar:  
⦿ Mesaj tarixçəsindən istifadəçinin mesajını göstərir. Ad, ID və ya cavab verərək istifadə olunur.  
Yalnız bot köməkçiləri üçün keçərlidir.

Nümunələr:  
⦿ /sm istifadəçi_adı  
⦿ /sm istifadəçi_ID  
⦿ /sm [mesaja cavab ver]
"""

    HELP_Couples = """Cütlüklər

Cütlüklər ƏMRLƏRİ:

/couples - 2 istifadəçi seçin və onların adlarını cütlük kimi göstərin.
"""

    HELP_Extra = """Əlavə

Əlavə ƏMRLƏR:

⦿ /tgm ➠ Fotoşəkili (5 MB-dən kiçik) yükləyib link təqdim edir.  
⦿ /paste ➠ Mətn hissəsini yükləyib link təqdim edir.  
⦿ /tr ➠ Mətn tərcümə edir.
"""

    HELP_Action = """Funksiyaları

Funksiyaları ƏMRLƏRİ:

» Ban və Səssizlik üçün mövcud əmrlər:

 ❍ /kickme: Komandanı icra edən istifadəçini qrupdan çıxarır.

Yalnız adminlər üçün:  
 ❍ /ban <istifadəçi adı>: İstifadəçini bloklayır.  
 ❍ /sban <istifadəçi adı>: Səssizcə istifadəçini bloklayır (cavabı silir).  
 ❍ /tban <istifadəçi adı> x(m/s/g): İstifadəçini müəyyən müddətə bloklayır.  
 ❍ /unban <istifadəçi adı>: İstifadəçini blokdan çıxarır.  
 ❍ /kick <istifadəçi adı>: İstifadəçini qrupdan çıxarır.  
 ❍ /mute <istifadəçi adı>: İstifadəçini səssiz edir.  
 ❍ /tmute <istifadəçi adı> x(m/s/g): İstifadəçini müəyyən müddətə səssiz edir.  
 ❍ /unmute <istifadəçi adı>: Səssizlik rejimini aradan qaldırır.
"""

    HELP_Search = """Axtarış

Axtarış ƏMRLƏRİ:

• /google <sorğu> : Google-da sorğu axtarışı edir.  
• /cek (/imgs) <sorğu> : Sorğuya uyğun şəkilləri göstərir.

Nümunə:  
/google pyrogram: Ən yaxşı 5 nəticəni qaytarır.
"""

    HELP_Font = """Şrift-çevirmə

Şrift-çevirmə modulu ilə mətnlərinizin şriftini dəyişə bilərsiniz.

Əmr:  
◌ /font [Mətn]
"""

    HELP_Bots = """Qrupdaki Botlar

Qrupdaki Botlar haqqında məlumat almaq üçün əmrlər:  
◌ /bots - Qrupdakı botların siyahısını göstərir.
"""

    HELP_TG = """Teleqraf 

Teleqraf ƏMRLƏRİ:

Telegraph linki ilə media yaradın!

◌ /tgm [istənilən media ilə cavab verin]  
◌ /tgt [istənilən media ilə cavab verin]
"""

    HELP_TD = """Doğru-Cəsarət

Doğru-Cəsarət ƏMRLƏRİ:  

◌ /truth : Təsadüfi bir sual təqdim edir.  
◌ /dare : Təsadüfi bir tapşırıq təqdim edir.
"""

    HELP_Quiz = """Suallar

Suallar ƏMRİ:

◌ /quiz - Təsadüfi sual əldə etmək üçün.
"""

    HELP_TTS = """Mətni-Sesə

Mətni-Sesə ƏMRLƏRİ:

❀ Mətn Səsləndirmə  
◌ /tts : [mətn]  
"""

    HELP_Radio = """Radio

Radio ƏMRLƏRİ:

◌ /radio - Səsli söhbətdə radio oynatmaq üçün.
"""

    HELP_Q = """Sitat Yarat

ƏMR:

◌ /q : Mesajdan sitat yaradın.
"""
