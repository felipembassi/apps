"""Builds the support and privacy pages for Felipe Bassi's apps (GitHub Pages, static, no cookies or analytics).

Run: python3 build.py   → <app>/{privacy,support}/<lang>.html plus an index.html per folder that picks the browser's language.
Edit the texts here, never the generated HTML.
"""
import html, json, pathlib

EMAIL = "felipe.mbassi@gmail.com"
ROOT = pathlib.Path(__file__).parent

APPS = {
    "purasorte": dict(name="Pura Sorte", langs=["pt-BR", "en", "es", "fr", "de", "it", "ja"]),
    "clockable": dict(name="Clockable", langs=["en", "pt-BR", "es", "fr", "de", "it", "ja"]),
    "lunido": dict(name="Lunido", langs=["en", "pt-BR", "pt-PT", "es", "fr", "de", "it", "nl", "ja"]),
}
LANG_NAMES = {"en": "English", "pt-BR": "Português (Brasil)", "pt-PT": "Português (Portugal)", "es": "Español", "fr": "Français",
              "de": "Deutsch", "it": "Italiano", "nl": "Nederlands", "ja": "日本語"}

# Shared sentences. {app} is the app name, {email} the contact link.
L = {
"en": dict(date="October 27, 2026", privacy="Privacy policy", support="Support", updated="Updated {date}.",
    lead="{app} doesn't collect, sell or share personal data. It has no ads, no analytics, no third-party SDKs and no account, and it doesn't track you across apps or websites.",
    stays="What stays on your device", icloud="If iCloud is on, it syncs through Apple in your private iCloud database, which the developer can't access.",
    purchases="Purchases", purchases_p="{app} Pro is a one-time purchase handled by Apple. The developer never receives your payment details.",
    children="Children", children_p="The app collects no data from anyone, including children.",
    changes="Changes", changes_p="If this policy changes, this page will show the new text and date.",
    contact="Contact", contact_p="Questions about privacy: {email}.",
    support_lead="Questions, problems or ideas? Email {email}. We usually reply within 2 business days.",
    faq="Common questions",
    restore_q="How do I get Pro back on a new device?", restore_a="Open Settings in the app and tap {restore} while signed in with the Apple ID you bought it with.",
    sync_q="My data doesn't show up on my other device.", sync_a="Check that both devices use the same Apple ID and that iCloud is on for {app} in the iOS Settings app (your name › iCloud). Syncing can take a few minutes.",
    other="Other languages", privacy_link="Privacy policy", support_link="Support"),
"pt-BR": dict(date="27 de outubro de 2026", privacy="Política de privacidade", support="Suporte", updated="Atualizada em {date}.",
    lead="O {app} não coleta, não vende e não compartilha dados pessoais. Não tem anúncios, ferramentas de análise, SDKs de terceiros nem conta, e não rastreia você entre apps ou sites.",
    stays="O que fica no seu aparelho", icloud="Se o iCloud estiver ativo, isso é sincronizado pela Apple no seu banco de dados privado do iCloud, ao qual o desenvolvedor não tem acesso.",
    purchases="Compras", purchases_p="O {app} Pro é uma compra única processada pela Apple. O desenvolvedor nunca recebe seus dados de pagamento.",
    children="Crianças", children_p="O app não coleta dados de ninguém, inclusive de crianças.",
    changes="Mudanças", changes_p="Se esta política mudar, esta página mostrará o novo texto e a nova data.",
    contact="Contato", contact_p="Dúvidas sobre privacidade: {email}.",
    support_lead="Dúvidas, problemas ou ideias? Escreva para {email}. Costumamos responder em até 2 dias úteis.",
    faq="Perguntas frequentes",
    restore_q="Como recupero o Pro num aparelho novo?", restore_a="Abra os Ajustes do app e toque em {restore}, com o mesmo Apple ID usado na compra.",
    sync_q="Meus dados não aparecem no meu outro aparelho.", sync_a="Confira se os dois aparelhos usam o mesmo Apple ID e se o iCloud está ativo para o {app} no app Ajustes do iOS (seu nome › iCloud). A sincronização pode levar alguns minutos.",
    other="Outros idiomas", privacy_link="Política de privacidade", support_link="Suporte"),
"pt-PT": dict(date="27 de outubro de 2026", privacy="Política de privacidade", support="Suporte", updated="Atualizada a {date}.",
    lead="O {app} não recolhe, não vende e não partilha dados pessoais. Não tem anúncios, ferramentas de análise, SDK de terceiros nem conta, e não o segue entre apps ou sites.",
    stays="O que fica no seu dispositivo", icloud="Se o iCloud estiver ativo, isto é sincronizado pela Apple na sua base de dados privada do iCloud, à qual o programador não tem acesso.",
    purchases="Compras", purchases_p="O {app} Pro é uma compra única processada pela Apple. O programador nunca recebe os seus dados de pagamento.",
    children="Crianças", children_p="A app não recolhe dados de ninguém, incluindo crianças.",
    changes="Alterações", changes_p="Se esta política mudar, esta página mostrará o novo texto e a nova data.",
    contact="Contacto", contact_p="Dúvidas sobre privacidade: {email}.",
    support_lead="Dúvidas, problemas ou ideias? Escreva para {email}. Costumamos responder em até 2 dias úteis.",
    faq="Perguntas frequentes",
    restore_q="Como recupero o Pro num dispositivo novo?", restore_a="Abra as Definições da app e toque em {restore}, com o mesmo ID Apple usado na compra.",
    sync_q="Os meus dados não aparecem no outro dispositivo.", sync_a="Confirme que os dois dispositivos usam o mesmo ID Apple e que o iCloud está ativo para o {app} na app Definições do iOS (o seu nome › iCloud). A sincronização pode demorar alguns minutos.",
    other="Outros idiomas", privacy_link="Política de privacidade", support_link="Suporte"),
"es": dict(date="27 de octubre de 2026", privacy="Política de privacidad", support="Soporte", updated="Actualizada el {date}.",
    lead="{app} no recopila, no vende y no comparte datos personales. No tiene anuncios, herramientas de análisis, SDK de terceros ni cuenta, y no te rastrea entre apps o sitios web.",
    stays="Lo que se queda en tu dispositivo", icloud="Si iCloud está activado, se sincroniza a través de Apple en tu base de datos privada de iCloud, a la que el desarrollador no tiene acceso.",
    purchases="Compras", purchases_p="{app} Pro es un pago único gestionado por Apple. El desarrollador nunca recibe tus datos de pago.",
    children="Niños", children_p="La app no recopila datos de nadie, tampoco de niños.",
    changes="Cambios", changes_p="Si esta política cambia, esta página mostrará el nuevo texto y la nueva fecha.",
    contact="Contacto", contact_p="Preguntas sobre privacidad: {email}.",
    support_lead="¿Preguntas, problemas o ideas? Escribe a {email}. Solemos responder en 2 días hábiles.",
    faq="Preguntas frecuentes",
    restore_q="¿Cómo recupero Pro en un dispositivo nuevo?", restore_a="Abre los Ajustes de la app y toca {restore} con el mismo Apple ID con el que compraste.",
    sync_q="Mis datos no aparecen en mi otro dispositivo.", sync_a="Comprueba que ambos dispositivos usan el mismo Apple ID y que iCloud está activado para {app} en la app Ajustes de iOS (tu nombre › iCloud). La sincronización puede tardar unos minutos.",
    other="Otros idiomas", privacy_link="Política de privacidad", support_link="Soporte"),
"fr": dict(date="27 octobre 2026", privacy="Politique de confidentialité", support="Assistance", updated="Mise à jour le {date}.",
    lead="{app} ne collecte, ne vend et ne partage aucune donnée personnelle. Pas de publicité, pas d'outil d'analyse, pas de SDK tiers, pas de compte, et aucun suivi entre apps ou sites web.",
    stays="Ce qui reste sur votre appareil", icloud="Si iCloud est activé, ces données sont synchronisées par Apple dans votre base de données iCloud privée, à laquelle le développeur n'a pas accès.",
    purchases="Achats", purchases_p="{app} Pro est un achat unique géré par Apple. Le développeur ne reçoit jamais vos informations de paiement.",
    children="Enfants", children_p="L'app ne collecte de données sur personne, y compris les enfants.",
    changes="Modifications", changes_p="Si cette politique change, cette page affichera le nouveau texte et la nouvelle date.",
    contact="Contact", contact_p="Questions sur la confidentialité : {email}.",
    support_lead="Une question, un problème, une idée ? Écrivez à {email}. Nous répondons en général sous 2 jours ouvrés.",
    faq="Questions fréquentes",
    restore_q="Comment récupérer Pro sur un nouvel appareil ?", restore_a="Ouvrez les Réglages de l'app et touchez {restore}, connecté avec l'identifiant Apple utilisé pour l'achat.",
    sync_q="Mes données n'apparaissent pas sur mon autre appareil.", sync_a="Vérifiez que les deux appareils utilisent le même identifiant Apple et qu'iCloud est activé pour {app} dans l'app Réglages d'iOS (votre nom › iCloud). La synchronisation peut prendre quelques minutes.",
    other="Autres langues", privacy_link="Politique de confidentialité", support_link="Assistance"),
"de": dict(date="27. Oktober 2026", privacy="Datenschutzerklärung", support="Support", updated="Stand: {date}.",
    lead="{app} erhebt, verkauft und teilt keine personenbezogenen Daten. Keine Werbung, keine Analyse-Tools, keine SDKs von Drittanbietern, kein Konto und kein Tracking über Apps oder Websites hinweg.",
    stays="Was auf deinem Gerät bleibt", icloud="Wenn iCloud aktiv ist, wird das über Apple in deiner privaten iCloud-Datenbank synchronisiert, auf die der Entwickler keinen Zugriff hat.",
    purchases="Käufe", purchases_p="{app} Pro ist ein Einmalkauf, den Apple abwickelt. Der Entwickler erhält deine Zahlungsdaten nie.",
    children="Kinder", children_p="Die App erhebt von niemandem Daten, auch nicht von Kindern.",
    changes="Änderungen", changes_p="Wenn sich diese Erklärung ändert, zeigt diese Seite den neuen Text und das neue Datum.",
    contact="Kontakt", contact_p="Fragen zum Datenschutz: {email}.",
    support_lead="Fragen, Probleme oder Ideen? Schreib an {email}. Wir antworten meist innerhalb von 2 Werktagen.",
    faq="Häufige Fragen",
    restore_q="Wie bekomme ich Pro auf einem neuen Gerät zurück?", restore_a="Öffne die Einstellungen der App und tippe auf „{restore}“, angemeldet mit der Apple-ID, mit der du gekauft hast.",
    sync_q="Meine Daten erscheinen nicht auf meinem anderen Gerät.", sync_a="Prüfe, ob beide Geräte dieselbe Apple-ID nutzen und iCloud für {app} in der iOS-App „Einstellungen“ aktiv ist (dein Name › iCloud). Die Synchronisierung kann ein paar Minuten dauern.",
    other="Andere Sprachen", privacy_link="Datenschutz", support_link="Support"),
"it": dict(date="27 ottobre 2026", privacy="Informativa sulla privacy", support="Assistenza", updated="Aggiornata il {date}.",
    lead="{app} non raccoglie, non vende e non condivide dati personali. Niente pubblicità, strumenti di analisi, SDK di terze parti o account, e nessun tracciamento tra app o siti web.",
    stays="Cosa resta sul tuo dispositivo", icloud="Se iCloud è attivo, questi dati si sincronizzano tramite Apple nel tuo database iCloud privato, a cui lo sviluppatore non ha accesso.",
    purchases="Acquisti", purchases_p="{app} Pro è un acquisto unico gestito da Apple. Lo sviluppatore non riceve mai i tuoi dati di pagamento.",
    children="Bambini", children_p="L'app non raccoglie dati di nessuno, nemmeno dei bambini.",
    changes="Modifiche", changes_p="Se questa informativa cambia, questa pagina mostrerà il nuovo testo e la nuova data.",
    contact="Contatti", contact_p="Domande sulla privacy: {email}.",
    support_lead="Domande, problemi o idee? Scrivi a {email}. Di solito rispondiamo entro 2 giorni lavorativi.",
    faq="Domande frequenti",
    restore_q="Come recupero Pro su un nuovo dispositivo?", restore_a="Apri le Impostazioni dell'app e tocca {restore}, con lo stesso ID Apple usato per l'acquisto.",
    sync_q="I miei dati non compaiono sull'altro dispositivo.", sync_a="Verifica che entrambi i dispositivi usino lo stesso ID Apple e che iCloud sia attivo per {app} nell'app Impostazioni di iOS (il tuo nome › iCloud). La sincronizzazione può richiedere qualche minuto.",
    other="Altre lingue", privacy_link="Privacy", support_link="Assistenza"),
"nl": dict(date="27 oktober 2026", privacy="Privacybeleid", support="Ondersteuning", updated="Bijgewerkt op {date}.",
    lead="{app} verzamelt, verkoopt en deelt geen persoonsgegevens. Geen advertenties, geen analysetools, geen SDK's van derden, geen account en geen tracking via andere apps of websites.",
    stays="Wat op je apparaat blijft", icloud="Als iCloud aanstaat, wordt dit via Apple gesynchroniseerd in je privé-iCloud-database, waar de ontwikkelaar geen toegang toe heeft.",
    purchases="Aankopen", purchases_p="{app} Pro is een eenmalige aankoop die Apple afhandelt. De ontwikkelaar ontvangt je betaalgegevens nooit.",
    children="Kinderen", children_p="De app verzamelt van niemand gegevens, ook niet van kinderen.",
    changes="Wijzigingen", changes_p="Als dit beleid verandert, toont deze pagina de nieuwe tekst en datum.",
    contact="Contact", contact_p="Vragen over privacy: {email}.",
    support_lead="Vragen, problemen of ideeën? Mail naar {email}. We antwoorden meestal binnen 2 werkdagen.",
    faq="Veelgestelde vragen",
    restore_q="Hoe krijg ik Pro terug op een nieuw apparaat?", restore_a="Open Instellingen in de app en tik op {restore}, ingelogd met de Apple ID waarmee je hebt gekocht.",
    sync_q="Mijn gegevens verschijnen niet op mijn andere apparaat.", sync_a="Controleer of beide apparaten dezelfde Apple ID gebruiken en of iCloud aanstaat voor {app} in de iOS-app Instellingen (je naam › iCloud). Synchroniseren kan een paar minuten duren.",
    other="Andere talen", privacy_link="Privacy", support_link="Ondersteuning"),
"ja": dict(date="2026年10月27日", privacy="プライバシーポリシー", support="サポート", updated="最終更新日：{date}",
    lead="{app}は個人データを収集・販売・共有しません。広告、分析ツール、他社製SDK、アカウントはなく、アプリやウェブサイトをまたいだトラッキングも行いません。",
    stays="デバイスに保存されるもの", icloud="iCloudがオンの場合、Appleを通じてあなたの非公開のiCloudデータベースに同期されます。開発者はそこにアクセスできません。",
    purchases="購入", purchases_p="{app} ProはAppleが処理する買い切りの購入です。開発者が支払い情報を受け取ることはありません。",
    children="子どもについて", children_p="本アプリは、子どもを含め、誰のデータも収集しません。",
    changes="変更", changes_p="このポリシーを変更した場合は、このページに新しい内容と日付を掲載します。",
    contact="お問い合わせ", contact_p="プライバシーに関するご質問：{email}",
    support_lead="ご質問、不具合、ご意見は {email} までお送りください。通常2営業日以内にお返事します。",
    faq="よくある質問",
    restore_q="新しいデバイスでProを復元するには？", restore_a="購入時と同じApple IDでサインインした状態で、アプリの設定から「{restore}」をタップしてください。",
    sync_q="別のデバイスにデータが表示されません。", sync_a="両方のデバイスが同じApple IDを使っていて、iOSの設定アプリ（ユーザ名 › iCloud）で{app}のiCloudがオンになっているか確認してください。同期には数分かかることがあります。",
    other="ほかの言語", privacy_link="プライバシー", support_link="サポート"),
}

# Per app: what it keeps (first sentence of "What stays on your device"), extra privacy sections and support FAQ.
STAYS = {
"purasorte": {
    "en": "The draws you save and your settings stay on your iPhone or iPad.",
    "pt-BR": "Os sorteios que você salva e as suas preferências ficam no seu iPhone ou iPad.",
    "es": "Los sorteos que guardas y tus ajustes se quedan en tu iPhone o iPad.",
    "fr": "Les tirages que vous enregistrez et vos réglages restent sur votre iPhone ou iPad.",
    "de": "Deine gespeicherten Ziehungen und Einstellungen bleiben auf deinem iPhone oder iPad.",
    "it": "Le estrazioni che salvi e le tue impostazioni restano sul tuo iPhone o iPad.",
    "ja": "保存した抽選結果と設定は、あなたのiPhoneまたはiPadに保存されます。"},
"clockable": {
    "en": "Your jobs, shifts, breaks, pay rates and settings stay on your iPhone or iPad.",
    "pt-BR": "Seus empregos, turnos, pausas, valores por hora e preferências ficam no seu iPhone ou iPad.",
    "es": "Tus trabajos, turnos, pausas, tarifas por hora y ajustes se quedan en tu iPhone o iPad.",
    "fr": "Vos emplois, services, pauses, taux horaires et réglages restent sur votre iPhone ou iPad.",
    "de": "Deine Jobs, Schichten, Pausen, Stundenlöhne und Einstellungen bleiben auf deinem iPhone oder iPad.",
    "it": "I tuoi lavori, turni, pause, tariffe orarie e impostazioni restano sul tuo iPhone o iPad.",
    "ja": "勤務先、シフト、休憩、時給、設定は、あなたのiPhoneまたはiPadに保存されます。"},
"lunido": {
    "en": "Your list, the due date, what you've bought or been given, the hospital bag and your settings stay on your iPhone.",
    "pt-BR": "Sua lista, a data prevista do parto, o que você comprou ou ganhou, a mala da maternidade e as suas preferências ficam no seu iPhone.",
    "pt-PT": "A sua lista, a data prevista do parto, o que comprou ou recebeu, o saco da maternidade e as suas preferências ficam no seu iPhone.",
    "es": "Tu lista, la fecha prevista de parto, lo que compraste o te regalaron, la bolsa del hospital y tus ajustes se quedan en tu iPhone.",
    "fr": "Votre liste, la date prévue d'accouchement, ce que vous avez acheté ou reçu, la valise de maternité et vos réglages restent sur votre iPhone.",
    "de": "Deine Liste, der Geburtstermin, was du gekauft oder geschenkt bekommen hast, die Kliniktasche und deine Einstellungen bleiben auf deinem iPhone.",
    "it": "La tua lista, la data presunta del parto, ciò che hai comprato o ricevuto in regalo, la borsa per l'ospedale e le tue impostazioni restano sul tuo iPhone.",
    "nl": "Je lijst, de uitgerekende datum, wat je hebt gekocht of gekregen, de vluchtkoffer en je instellingen blijven op je iPhone.",
    "ja": "リスト、出産予定日、購入したものやもらったもの、入院バッグ、設定は、あなたのiPhoneに保存されます。"},
}

EXTRA = {
"clockable": {
    "en": [("Exports", "CSV and PDF files are created on your device and go only where you choose to share them.")],
    "pt-BR": [("Exportações", "Os arquivos CSV e PDF são criados no seu aparelho e vão só para onde você escolher compartilhar.")],
    "es": [("Exportaciones", "Los archivos CSV y PDF se crean en tu dispositivo y solo van adonde decidas compartirlos.")],
    "fr": [("Exports", "Les fichiers CSV et PDF sont créés sur votre appareil et ne vont que là où vous choisissez de les partager.")],
    "de": [("Exporte", "CSV- und PDF-Dateien entstehen auf deinem Gerät und gehen nur dorthin, wo du sie teilst.")],
    "it": [("Esportazioni", "I file CSV e PDF vengono creati sul tuo dispositivo e vanno solo dove scegli di condividerli.")],
    "ja": [("書き出し", "CSVとPDFのファイルはデバイス上で作成され、あなたが共有を選んだ先にだけ送られます。")]},
"lunido": {
    "en": [("Reminders", "Reminders are scheduled on your iPhone by iOS. Nothing is sent to us."),
           ("Your region", "You choose your region yourself. The app never asks for your location.")],
    "pt-BR": [("Lembretes", "Os lembretes são agendados no seu iPhone pelo iOS. Nada é enviado para nós."),
              ("Sua região", "Você escolhe a sua região. O app nunca pede a sua localização.")],
    "pt-PT": [("Lembretes", "Os lembretes são agendados no seu iPhone pelo iOS. Nada nos é enviado."),
              ("A sua região", "É o utilizador que escolhe a região. A app nunca pede a sua localização.")],
    "es": [("Recordatorios", "iOS programa los recordatorios en tu iPhone. No se nos envía nada."),
           ("Tu región", "Tú eliges tu región. La app nunca pide tu ubicación.")],
    "fr": [("Rappels", "Les rappels sont programmés sur votre iPhone par iOS. Rien ne nous est envoyé."),
           ("Votre région", "Vous choisissez vous-même votre région. L'app ne demande jamais votre position.")],
    "de": [("Erinnerungen", "Erinnerungen plant iOS auf deinem iPhone. Nichts wird an uns gesendet."),
           ("Deine Region", "Du wählst deine Region selbst. Die App fragt nie nach deinem Standort.")],
    "it": [("Promemoria", "I promemoria sono programmati da iOS sul tuo iPhone. Non ci viene inviato nulla."),
           ("La tua regione", "Scegli tu la tua regione. L'app non chiede mai la tua posizione.")],
    "nl": [("Herinneringen", "Herinneringen worden door iOS op je iPhone ingepland. Er wordt niets naar ons gestuurd."),
           ("Je regio", "Je kiest zelf je regio. De app vraagt nooit om je locatie.")],
    "ja": [("リマインダー", "リマインダーはiOSがあなたのiPhone上で設定します。私たちに送信されるものはありません。"),
           ("地域", "地域はあなた自身が選びます。アプリが位置情報を求めることはありません。")]},
}

# The Pro restore button, as each app labels it (Lunido's is singular).
RESTORE = {
    "en": "Restore Purchases", "pt-BR": "Restaurar compras", "pt-PT": "Restaurar compras", "es": "Restaurar compras",
    "fr": "Restaurer les achats", "de": "Käufe wiederherstellen", "it": "Ripristina acquisti", "nl": "Aankopen herstellen", "ja": "購入を復元",
}
RESTORE_LUNIDO = {
    "en": "Restore purchase", "pt-BR": "Restaurar compra", "pt-PT": "Restaurar compra", "es": "Restaurar compra", "fr": "Restaurer l’achat",
    "de": "Kauf wiederherstellen", "it": "Ripristina acquisto", "nl": "Herstel aankoop", "ja": "購入を復元",
}

# Where the restore button isn't on the Settings screen itself, the full answer.
RESTORE_ANSWER = {
"clockable": {
    "en": "In the app, go to Settings › Clockable Pro and tap Restore Purchases while signed in with the Apple ID you bought it with.",
    "pt-BR": "No app, vá em Ajustes › Clockable Pro e toque em Restaurar compras, com o mesmo Apple ID usado na compra.",
    "es": "En la app, ve a Ajustes › Clockable Pro y toca Restaurar compras con el mismo Apple ID con el que compraste.",
    "fr": "Dans l'app, allez dans Réglages › Clockable Pro et touchez Restaurer les achats, connecté avec l'identifiant Apple utilisé pour l'achat.",
    "de": "Öffne in der App Einstellungen › Clockable Pro und tippe auf „Käufe wiederherstellen“, angemeldet mit der Apple-ID, mit der du gekauft hast.",
    "it": "Nell'app, vai in Impostazioni › Clockable Pro e tocca Ripristina acquisti, con lo stesso ID Apple usato per l'acquisto.",
    "ja": "購入時と同じApple IDでサインインした状態で、アプリの「設定 › Clockable Pro」から「購入を復元」をタップしてください。"},
}

FAQ = {
"purasorte": {
    "en": [("Are the numbers really random?", "Yes. They come from the system's cryptographic random generator. In the Proof tab you can run up to 1 million draws and see that no number is favored."),
           ("Does the app improve my odds?", "No. No app can: every combination is equally likely. Pura Sorte doesn't sell tickets and isn't affiliated with any lottery operator.")],
    "pt-BR": [("Os números são aleatórios mesmo?", "Sim. Eles vêm do gerador aleatório criptográfico do sistema. Na aba Prova você roda até 1 milhão de sorteios e vê que nenhum número é favorecido."),
              ("O app aumenta minhas chances?", "Não. Nenhum app aumenta: toda combinação tem a mesma chance. O Pura Sorte não vende apostas e não tem vínculo com a CAIXA nem com outras operadoras de loteria.")],
    "es": [("¿Los números son realmente aleatorios?", "Sí. Vienen del generador aleatorio criptográfico del sistema. En la pestaña Prueba puedes ejecutar hasta 1 millón de sorteos y ver que ningún número sale favorecido."),
           ("¿La app aumenta mis probabilidades?", "No. Ninguna app puede: todas las combinaciones tienen la misma probabilidad. Pura Sorte no vende apuestas y no tiene vínculo con ningún operador de lotería.")],
    "fr": [("Les numéros sont-ils vraiment aléatoires ?", "Oui. Ils viennent du générateur aléatoire cryptographique du système. Dans l'onglet Preuve, lancez jusqu'à 1 million de tirages et constatez qu'aucun numéro n'est favorisé."),
           ("L'app augmente-t-elle mes chances ?", "Non. Aucune app ne le peut : toutes les combinaisons ont la même probabilité. Pura Sorte ne vend pas de paris et n'a aucun lien avec un opérateur de loterie.")],
    "de": [("Sind die Zahlen wirklich zufällig?", "Ja. Sie stammen aus dem kryptografischen Zufallsgenerator des Systems. Im Tab „Beweis“ kannst du bis zu 1 Million Ziehungen starten und sehen, dass keine Zahl bevorzugt wird."),
           ("Erhöht die App meine Chancen?", "Nein. Das kann keine App: Jede Kombination ist gleich wahrscheinlich. Pura Sorte verkauft keine Tipps und ist mit keinem Lotterieveranstalter verbunden.")],
    "it": [("I numeri sono davvero casuali?", "Sì. Vengono dal generatore casuale crittografico del sistema. Nella scheda Prova puoi eseguire fino a 1 milione di estrazioni e vedere che nessun numero è favorito."),
           ("L'app aumenta le mie probabilità?", "No. Nessuna app può farlo: ogni combinazione ha la stessa probabilità. Pura Sorte non vende giocate e non è legata ad alcun operatore di lotterie.")],
    "ja": [("番号は本当にランダムですか？", "はい。システムの暗号用乱数生成器から作られます。「検証」タブで最大100万回抽選し、どの数字も優遇されていないことを確かめられます。"),
           ("当選確率は上がりますか？", "いいえ。どのアプリにもできません。どの組み合わせも同じ確率です。Pura Sorteはくじを販売せず、宝くじ運営者とも関係ありません。")]},
"clockable": {
    "en": [("How do I export my hours?", "On the Summary screen, tap Export CSV (free) or Export PDF (Pro). Each one opens the share sheet."),
           ("Is this an official time clock?", "No. Clockable is a personal record of your own hours. For payroll, your employer's records are the official ones.")],
    "pt-BR": [("Como exporto minhas horas?", "Na tela Resumo, toque em Exportar CSV (grátis) ou Exportar PDF (Pro). Cada um abre a janela de compartilhamento."),
              ("É um ponto eletrônico oficial?", "Não. O Clockable é um controle pessoal das suas horas. Para a folha de pagamento, vale o registro oficial do empregador.")],
    "es": [("¿Cómo exporto mis horas?", "En la pantalla Resumen, toca Exportar CSV (gratis) o Exportar PDF (Pro). Cada opción abre la hoja para compartir."),
           ("¿Es un control horario oficial?", "No. Clockable es un registro personal de tus horas. Para la nómina, valen los registros de tu empleador.")],
    "fr": [("Comment exporter mes heures ?", "Dans l'écran Résumé, touchez Exporter en CSV (gratuit) ou Exporter en PDF (Pro). Chacun ouvre la feuille de partage."),
           ("Est-ce une pointeuse officielle ?", "Non. Clockable est un relevé personnel de vos heures. Pour la paie, ce sont les registres de votre employeur qui font foi.")],
    "de": [("Wie exportiere ich meine Stunden?", "Tippe in der Übersicht auf „Als CSV exportieren“ (gratis) oder „Als PDF exportieren“ (Pro). Beides öffnet das Teilen-Menü."),
           ("Ist das eine offizielle Zeiterfassung?", "Nein. Clockable ist eine persönliche Aufzeichnung deiner Stunden. Für die Lohnabrechnung zählen die Unterlagen deines Arbeitgebers.")],
    "it": [("Come esporto le mie ore?", "Nella schermata Riepilogo, tocca Esporta CSV (gratis) o Esporta PDF (Pro). Ognuno apre il foglio di condivisione."),
           ("È un rilevatore presenze ufficiale?", "No. Clockable è un registro personale delle tue ore. Per la busta paga valgono i registri del datore di lavoro.")],
    "ja": [("勤務時間を書き出すには？", "「集計」画面で「CSVを書き出す」（無料）または「PDFを書き出す」（Pro）をタップすると、共有シートが開きます。"),
           ("公式のタイムカードですか？", "いいえ。Clockableはご自身の勤務時間の個人的な記録です。給与計算には勤務先の公式記録が使われます。")]},
"lunido": {
    "en": [("The list doesn't fit my country or region.", "In Settings, tap Suggest a list correction and tell us what to change."),
           ("Is this medical advice?", "No. Lunido is a shopping and packing list. Safety notes cite official sources; for health questions, talk to your doctor or midwife.")],
    "pt-BR": [("A lista não serve para o meu país ou região.", "Nos Ajustes, toque em Sugerir correção da lista e conte o que mudar."),
              ("Isso é orientação médica?", "Não. O Lunido é uma lista de compras e da mala. As notas de segurança citam fontes oficiais; para dúvidas de saúde, fale com seu médico ou sua obstetriz.")],
    "pt-PT": [("A lista não se adequa ao meu país ou região.", "Nas Definições, toque em Sugerir uma correção à lista e diga-nos o que mudar."),
              ("Isto é aconselhamento médico?", "Não. O Lunido é uma lista de compras e do saco da maternidade. As notas de segurança citam fontes oficiais; para dúvidas de saúde, fale com o seu médico ou enfermeiro.")],
    "es": [("La lista no encaja con mi país o región.", "En Ajustes, toca Sugerir una corrección de la lista y cuéntanos qué cambiar."),
           ("¿Esto es consejo médico?", "No. Lunido es una lista de compras y de la bolsa del hospital. Las notas de seguridad citan fuentes oficiales; para dudas de salud, habla con tu médico o matrona.")],
    "fr": [("La liste ne correspond pas à mon pays ou ma région.", "Dans Réglages, touchez Suggérer une correction de la liste et dites-nous quoi changer."),
           ("Est-ce un avis médical ?", "Non. Lunido est une liste d'achats et de valise. Les notes de sécurité citent des sources officielles ; pour les questions de santé, parlez à votre médecin ou à votre sage-femme.")],
    "de": [("Die Liste passt nicht zu meinem Land oder meiner Region.", "Tippe in den Einstellungen auf „Korrektur der Liste vorschlagen“ und sag uns, was wir ändern sollen."),
           ("Ist das medizinischer Rat?", "Nein. Lunido ist eine Einkaufs- und Packliste. Sicherheitshinweise nennen offizielle Quellen; bei Gesundheitsfragen sprich mit deiner Ärztin oder Hebamme.")],
    "it": [("La lista non va bene per il mio paese o la mia regione.", "In Impostazioni, tocca Suggerisci una correzione alla lista e dicci cosa cambiare."),
           ("È un consiglio medico?", "No. Lunido è una lista di acquisti e della borsa per l'ospedale. Le note di sicurezza citano fonti ufficiali; per domande sulla salute, parla con il tuo medico o la tua ostetrica.")],
    "nl": [("De lijst past niet bij mijn land of regio.", "Tik in Instellingen op „Stel een correctie voor de lijst voor” en vertel ons wat er anders moet."),
           ("Is dit medisch advies?", "Nee. Lunido is een boodschappen- en paklijst. Veiligheidstips noemen officiële bronnen; met vragen over gezondheid ga je naar je arts of verloskundige.")],
    "ja": [("リストが自分の国や地域に合いません。", "設定の「リストの修正を提案」をタップして、変えてほしい点をお知らせください。"),
           ("医療的な助言ですか？", "いいえ。Lunidoは買い物と入院準備のリストです。安全に関するメモは公的な情報源を示しています。健康についてのご質問は、医師や助産師にご相談ください。")]},
}

PAGE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{app} · {title}</title>
<link rel="icon" href="../icon.png">
<link rel="stylesheet" href="../../style.css">
</head>
<body>
<header><img src="../icon.png" alt="" width="88" height="88"><h1>{app}</h1><p>{title}</p></header>
<main>
<section>
{body}
</section>
<nav><a href="../{other_doc}/{lang}.html">{other_label}</a></nav>
<footer><span>{other}:</span> {langs}</footer>
</main>
</body>
</html>
"""

def esc(s): return html.escape(s, quote=False)

def build_page(slug, app, lang, doc):
    t = L[lang]
    mail = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
    parts = []
    if doc == "privacy":
        parts.append(f"<p class=\"muted\">{esc(t['updated'].format(date=t['date']))}</p>")
        parts.append(f"<p class=\"lead\">{esc(t['lead'].format(app=app))}</p>")
        sections = [(t["stays"], STAYS[slug][lang] + " " + t["icloud"])] + EXTRA.get(slug, {}).get(lang, []) + [
            (t["purchases"], t["purchases_p"].format(app=app)), (t["children"], t["children_p"]), (t["changes"], t["changes_p"])]
        for h, p in sections:
            parts.append(f"<h2>{esc(h)}</h2>\n<p>{esc(p)}</p>")
        parts.append(f"<h2>{esc(t['contact'])}</h2>\n<p>{esc(t['contact_p']).replace('{email}', mail)}</p>")
        title, other_doc, other_label = t["privacy"], "support", t["support_link"]
    else:
        parts.append(f"<p class=\"lead\">{esc(t['support_lead']).replace('{email}', mail)}</p>")
        parts.append(f"<h2>{esc(t['faq'])}</h2>")
        restore = (RESTORE_LUNIDO if slug == "lunido" else RESTORE)[lang]
        restore_a = RESTORE_ANSWER.get(slug, {}).get(lang) or t["restore_a"].format(restore=restore)
        for q, a in [(t["restore_q"], restore_a), (t["sync_q"], t["sync_a"].format(app=app))] + FAQ[slug][lang]:
            parts.append(f"<h3>{esc(q)}</h3>\n<p>{esc(a)}</p>")
        title, other_doc, other_label = t["support"], "privacy", t["privacy_link"]
    current = ' aria-current="page"'
    langs = " · ".join(f'<a href="{l}.html" lang="{l}"{current if l == lang else ""}>{LANG_NAMES[l]}</a>' for l in APPS[slug]["langs"])
    return PAGE.format(lang=lang, app=esc(app), title=esc(title), body="\n".join(parts), other_doc=other_doc,
                       other_label=esc(other_label), other=esc(t["other"]), langs=langs)

CHOOSER = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{app}</title>
<link rel="icon" href="../icon.png">
<link rel="stylesheet" href="../../style.css">
<script>
// Opens the page in the browser's language (exact match first, then the same base language). No cookies.
(function () {{
  var langs = {langs_json};
  var wanted = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || "en"];
  for (var i = 0; i < wanted.length; i++) {{
    var w = wanted[i].toLowerCase(), base = w.split("-")[0];
    var hit = langs.filter(function (l) {{ return l.toLowerCase() === w; }})[0]
           || langs.filter(function (l) {{ return l.toLowerCase().split("-")[0] === base; }})[0];
    if (hit) {{ location.replace(hit + ".html"); return; }}
  }}
  location.replace((langs.indexOf("en") >= 0 ? "en" : langs[0]) + ".html");
}})();
</script>
</head>
<body>
<header><img src="../icon.png" alt="" width="88" height="88"><h1>{app}</h1></header>
<main><section><ul class="langs">{links}</ul></section></main>
</body>
</html>
"""

INDEX = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Apps by Felipe Bassi</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header><h1>Apps by Felipe Bassi</h1><p>Support and privacy</p></header>
<main>
{cards}
<footer><a href="mailto:{email}">{email}</a></footer>
</main>
</body>
</html>
"""

def main():
    cards = []
    for slug, info in APPS.items():
        app = info["name"]
        for doc in ("privacy", "support"):
            d = ROOT / slug / doc
            d.mkdir(parents=True, exist_ok=True)
            for lang in info["langs"]:
                (d / f"{lang}.html").write_text(build_page(slug, app, lang, doc))
            links = "".join(f'<li><a href="{l}.html" lang="{l}">{LANG_NAMES[l]}</a></li>' for l in info["langs"])
            (d / "index.html").write_text(CHOOSER.format(app=esc(app), langs_json=json.dumps(info["langs"]), links=links))
        cards.append(f'<section class="app"><img src="{slug}/icon.png" alt="" width="64" height="64"><div><h2>{esc(app)}</h2>'
                     f'<p><a href="{slug}/support/">Support</a> · <a href="{slug}/privacy/">Privacy policy</a></p></div></section>')
    (ROOT / "index.html").write_text(INDEX.format(cards="\n".join(cards), email=EMAIL))
    print("built", sum(len(a["langs"]) * 2 for a in APPS.values()), "pages")

if __name__ == "__main__":
    main()
