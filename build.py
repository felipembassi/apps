"""Builds the support and privacy pages for Felipe Bassi's apps (GitHub Pages, static, no cookies or analytics).

Run: python3 build.py   → <app>/{privacy,support}/<lang>.html and lunido/android/{privacy,delete-account}/<lang>.html,
plus an index.html per folder that picks the browser's language.
Edit the texts here, never the generated HTML.
"""
import html, json, pathlib

EMAIL = "felipe.mbassi@gmail.com"
ROOT = pathlib.Path(__file__).parent

APPS = {
    "purasorte": dict(name="Pura Sorte", langs=["pt-BR", "en", "es", "fr", "de", "it", "ja"]),
    "hourbee": dict(name="Hourbee", langs=["en", "pt-BR", "es", "fr", "de", "it", "ja"]),
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
"hourbee": {
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
"hourbee": {
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
"hourbee": {
    "en": "In the app, go to Settings › Hourbee Pro and tap Restore Purchases while signed in with the Apple ID you bought it with.",
    "pt-BR": "No app, vá em Ajustes › Hourbee Pro e toque em Restaurar compras, com o mesmo Apple ID usado na compra.",
    "es": "En la app, ve a Ajustes › Hourbee Pro y toca Restaurar compras con el mismo Apple ID con el que compraste.",
    "fr": "Dans l'app, allez dans Réglages › Hourbee Pro et touchez Restaurer les achats, connecté avec l'identifiant Apple utilisé pour l'achat.",
    "de": "Öffne in der App Einstellungen › Hourbee Pro und tippe auf „Käufe wiederherstellen“, angemeldet mit der Apple-ID, mit der du gekauft hast.",
    "it": "Nell'app, vai in Impostazioni › Hourbee Pro e tocca Ripristina acquisti, con lo stesso ID Apple usato per l'acquisto.",
    "ja": "購入時と同じApple IDでサインインした状態で、アプリの「設定 › Hourbee Pro」から「購入を復元」をタップしてください。"},
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
"hourbee": {
    "en": [("How do I export my hours?", "On the Summary screen, tap Export CSV (free) or Export PDF (Pro). Each one opens the share sheet."),
           ("Is this an official time clock?", "No. Hourbee is a personal record of your own hours. For payroll, your employer's records are the official ones.")],
    "pt-BR": [("Como exporto minhas horas?", "Na tela Resumo, toque em Exportar CSV (grátis) ou Exportar PDF (Pro). Cada um abre a janela de compartilhamento."),
              ("É um ponto eletrônico oficial?", "Não. O Hourbee é um controle pessoal das suas horas. Para a folha de pagamento, vale o registro oficial do empregador.")],
    "es": [("¿Cómo exporto mis horas?", "En la pantalla Resumen, toca Exportar CSV (gratis) o Exportar PDF (Pro). Cada opción abre la hoja para compartir."),
           ("¿Es un control horario oficial?", "No. Hourbee es un registro personal de tus horas. Para la nómina, valen los registros de tu empleador.")],
    "fr": [("Comment exporter mes heures ?", "Dans l'écran Résumé, touchez Exporter en CSV (gratuit) ou Exporter en PDF (Pro). Chacun ouvre la feuille de partage."),
           ("Est-ce une pointeuse officielle ?", "Non. Hourbee est un relevé personnel de vos heures. Pour la paie, ce sont les registres de votre employeur qui font foi.")],
    "de": [("Wie exportiere ich meine Stunden?", "Tippe in der Übersicht auf „Als CSV exportieren“ (gratis) oder „Als PDF exportieren“ (Pro). Beides öffnet das Teilen-Menü."),
           ("Ist das eine offizielle Zeiterfassung?", "Nein. Hourbee ist eine persönliche Aufzeichnung deiner Stunden. Für die Lohnabrechnung zählen die Unterlagen deines Arbeitgebers.")],
    "it": [("Come esporto le mie ore?", "Nella schermata Riepilogo, tocca Esporta CSV (gratis) o Esporta PDF (Pro). Ognuno apre il foglio di condivisione."),
           ("È un rilevatore presenze ufficiale?", "No. Hourbee è un registro personale delle tue ore. Per la busta paga valgono i registri del datore di lavoro.")],
    "ja": [("勤務時間を書き出すには？", "「集計」画面で「CSVを書き出す」（無料）または「PDFを書き出す」（Pro）をタップすると、共有シートが開きます。"),
           ("公式のタイムカードですか？", "いいえ。Hourbeeはご自身の勤務時間の個人的な記録です。給与計算には勤務先の公式記録が使われます。")]},
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

# Lunido for Android: local-first like iOS, but sharing (Pro, Android ↔ Android) goes through Google sign-in and
# Firebase, so it gets its own privacy policy and the account deletion page Google Play asks for. Facts from
# ~/Documents/Workspace/Android/Lunido (sync/Cloud.kt, sync/SharedPlans.kt, firebase/firestore.rules); the menu
# paths are the app's own labels.
ANDROID = {
"en": dict(
    lead="Lunido for Android has no ads, no analytics and no tracking, and it never sells your data. You don't need an account: your list stays on your phone unless you choose to share it.",
    stays_p="Your list, the due date, what you've bought or been given, the hospital bag and your settings stay on your phone. If Android backup is on, Android keeps a copy in your Google account so you can move everything to a new phone. The developer can't access that backup.",
    share_h="Sharing the list (optional)",
    share_p="Sharing is part of Lunido Pro and works only between Android phones. To share or join a list, each person signs in with Google. Lunido then uses two Google Firebase services. Firebase Authentication receives your name, email address, Google profile picture link and a user ID, and sees your IP address to protect sign-in from abuse. Cloud Firestore stores the shared plan: the baby's nickname, the due date, climate and region, item names, quantities, statuses, prices, the budget, gifts with the names of who gave them, notes, and whether the plan's creator has Pro. On a new phone, sign in with the same Google account to get the shared list back.",
    access_p="Only the people in a plan can read or edit it. Invite codes have 8 characters and expire after 7 days. The data travels encrypted, and Google processes it for us under the Firebase terms. It's used only to keep the list in sync between your phones: never for ads or profiling, and it isn't shared with anyone else.",
    reminders_p="Reminders are scheduled on your phone by Android. Nothing is sent to us.",
    delete_h="Deleting your data",
    delete_p="Shared data stays in Firebase only while the plan exists: it's deleted when the plan's creator stops sharing, uses Delete everything or deletes their account. Settings › Share the list › Delete account deletes the plans you created, takes you out of the ones you joined and then deletes your account. Settings › Delete everything removes the list from your phone. Can't use the app? See {delete_link}.",
    purchases_p="Lunido Pro is a one-time purchase handled by Google Play. The developer never receives your payment details.",
    children_p="Lunido is made for adults preparing for a baby. We don't knowingly collect data from children.",
    delete_title="Delete your account",
    delete_lead="You only have a Lunido account if you signed in with Google to share your list on Android. Without one, everything is on your phone: Settings › Delete everything, or uninstalling the app, removes it.",
    inapp_h="In the app", inapp_p="Open Settings › Share the list, tap Delete account (it shows while you're signed in) and confirm. Lunido first asks you to confirm your Google account; if you cancel, nothing is deleted.",
    gone_h="What is deleted", gone_p="Your Lunido account: the name, email address, profile picture link and user ID in Firebase Authentication. The shared plans you created: the plan, all its items and gifts, and its invite codes; the people you shared with go back to their own list. Plans you joined: you're removed from them.",
    kept_h="What is kept", kept_p="The list on your phone stays until you delete it there. A plan you joined belongs to the person who created it, so what you added to it stays until they delete it. Google Play keeps its own record of your Pro purchase. We keep no other copy; Google then clears the data from Firebase's backups over time.",
    email_h="Without the app", email_p="Lost your phone, or the app couldn't finish? Email {email} from the Google address you signed in with and ask us to delete your Lunido account. We'll delete it, with the shared plans you created, within 30 days and reply when it's done."),
"pt-BR": dict(
    lead="O Lunido para Android não tem anúncios, ferramentas de análise nem rastreamento, e nunca vende os seus dados. Você não precisa de conta: sua lista fica no seu celular, a menos que você decida compartilhá-la.",
    stays_p="Sua lista, a data prevista do parto, o que você comprou ou ganhou, a mala da maternidade e as suas preferências ficam no seu celular. Se o backup do Android estiver ativo, o Android guarda uma cópia na sua conta Google para você levar tudo para um celular novo. O desenvolvedor não tem acesso a esse backup.",
    share_h="Compartilhar a lista (opcional)",
    share_p="O compartilhamento faz parte do Lunido Pro e funciona só entre celulares Android. Para compartilhar ou entrar numa lista, cada pessoa entra com a conta Google. O Lunido usa então dois serviços do Google Firebase. O Firebase Authentication recebe seu nome, seu e-mail, o link da sua foto de perfil do Google e um ID de usuário, e vê seu endereço IP para proteger o login contra abusos. O Cloud Firestore guarda o plano compartilhado: o apelido do bebê, a data prevista do parto, o clima e a região, os nomes dos itens, quantidades, status, preços, o orçamento, os presentes com o nome de quem deu, as anotações e se quem criou o plano tem o Pro. Num celular novo, entre com a mesma conta Google para ver a lista compartilhada de novo.",
    access_p="Só as pessoas de um plano podem ver ou editar esse plano. Os códigos de convite têm 8 caracteres e expiram em 7 dias. Os dados trafegam criptografados e o Google os processa para nós nos termos do Firebase. Eles servem só para manter a lista igual nos celulares de vocês: nunca para anúncios ou perfis, e não são compartilhados com mais ninguém.",
    reminders_p="Os lembretes são agendados no seu celular pelo Android. Nada é enviado para nós.",
    delete_h="Apagar seus dados",
    delete_p="Os dados compartilhados ficam no Firebase só enquanto o plano existir: são apagados quando quem o criou para de compartilhar, usa Apagar tudo ou apaga a conta. Ajustes › Compartilhar a lista › Apagar conta apaga os planos que você criou, tira você dos planos em que entrou e depois apaga a sua conta. Ajustes › Apagar tudo remove a lista do seu celular. Sem acesso ao app? Veja {delete_link}.",
    purchases_p="O Lunido Pro é uma compra única processada pelo Google Play. O desenvolvedor nunca recebe seus dados de pagamento.",
    children_p="O Lunido é feito para adultos que estão esperando um bebê. Não coletamos intencionalmente dados de crianças.",
    delete_title="Apagar sua conta",
    delete_lead="Você só tem uma conta no Lunido se entrou com o Google para compartilhar a lista no Android. Sem conta, tudo fica no seu celular: Ajustes › Apagar tudo, ou desinstalar o app, remove tudo.",
    inapp_h="No app", inapp_p="Abra Ajustes › Compartilhar a lista, toque em Apagar conta (aparece enquanto você está conectado) e confirme. Antes, o Lunido pede para você confirmar sua conta Google; se você cancelar, nada é apagado.",
    gone_h="O que é apagado", gone_p="Sua conta do Lunido: o nome, o e-mail, o link da foto de perfil e o ID de usuário no Firebase Authentication. Os planos compartilhados que você criou: o plano, todos os itens e presentes e os códigos de convite; quem estava com você volta para a própria lista. Os planos em que você entrou: você sai deles.",
    kept_h="O que fica", kept_p="A lista no seu celular fica até você apagá-la lá. Um plano em que você entrou pertence a quem o criou, então o que você adicionou continua nele até essa pessoa apagá-lo. O Google Play guarda o próprio registro da sua compra do Pro. Não guardamos nenhuma outra cópia; depois, o Google limpa esses dados dos backups do Firebase com o tempo.",
    email_h="Sem o app", email_p="Perdeu o celular ou o app não conseguiu terminar? Escreva para {email} a partir do e-mail Google com que você entrou e peça para apagarmos sua conta do Lunido. Vamos apagá-la, junto com os planos compartilhados que você criou, em até 30 dias e responder quando estiver feito."),
"pt-PT": dict(
    lead="O Lunido para Android não tem anúncios, ferramentas de análise nem rastreamento, e nunca vende os seus dados. Não precisa de conta: a sua lista fica no seu telemóvel, a não ser que decida partilhá-la.",
    stays_p="A sua lista, a data prevista do parto, o que comprou ou recebeu, o saco da maternidade e as suas preferências ficam no seu telemóvel. Se a cópia de segurança do Android estiver ativa, o Android guarda uma cópia na sua conta Google para poder passar tudo para um telemóvel novo. O programador não tem acesso a essa cópia.",
    share_h="Partilhar a lista (opcional)",
    share_p="A partilha faz parte do Lunido Pro e só funciona entre telemóveis Android. Para partilhar ou entrar numa lista, cada pessoa inicia sessão com a conta Google. O Lunido usa então dois serviços do Google Firebase. O Firebase Authentication recebe o seu nome, o endereço de e-mail, a ligação para a sua foto de perfil Google e um ID de utilizador, e vê o seu endereço IP para proteger o início de sessão contra abusos. O Cloud Firestore guarda o plano partilhado: a alcunha do bebé, a data prevista do parto, o clima e a região, os nomes dos artigos, quantidades, estados, preços, o orçamento, as prendas com o nome de quem as deu, as notas e se quem criou o plano tem o Pro. Num telemóvel novo, inicie sessão com a mesma conta Google para voltar a ver a lista partilhada.",
    access_p="Só as pessoas de um plano o podem ver ou editar. Os códigos de convite têm 8 caracteres e expiram ao fim de 7 dias. Os dados circulam encriptados e a Google trata-os por nossa conta, nos termos do Firebase. Servem apenas para manter a lista igual nos vossos telemóveis: nunca para publicidade ou perfis, e não são partilhados com mais ninguém.",
    reminders_p="Os lembretes são agendados no seu telemóvel pelo Android. Nada nos é enviado.",
    delete_h="Apagar os seus dados",
    delete_p="Os dados partilhados ficam no Firebase apenas enquanto o plano existir: são apagados quando quem o criou deixa de partilhar, usa Apagar tudo ou apaga a conta. Definições › Partilhar a lista › Apagar conta apaga os planos que criou, retira-o dos planos em que entrou e depois apaga a sua conta. Definições › Apagar tudo remove a lista do seu telemóvel. Não consegue usar a app? Veja {delete_link}.",
    purchases_p="O Lunido Pro é uma compra única processada pelo Google Play. O programador nunca recebe os seus dados de pagamento.",
    children_p="O Lunido destina-se a adultos que estão à espera de um bebé. Não recolhemos intencionalmente dados de crianças.",
    delete_title="Apagar a sua conta",
    delete_lead="Só tem uma conta no Lunido se iniciou sessão com a Google para partilhar a lista no Android. Sem conta, tudo fica no seu telemóvel: Definições › Apagar tudo, ou desinstalar a app, remove tudo.",
    inapp_h="Na app", inapp_p="Abra Definições › Partilhar a lista, toque em Apagar conta (aparece enquanto tiver sessão iniciada) e confirme. Antes, o Lunido pede-lhe que confirme a sua conta Google; se cancelar, nada é apagado.",
    gone_h="O que é apagado", gone_p="A sua conta do Lunido: o nome, o endereço de e-mail, a ligação para a foto de perfil e o ID de utilizador no Firebase Authentication. Os planos partilhados que criou: o plano, todos os artigos e prendas e os códigos de convite; as pessoas com quem partilhou voltam à própria lista. Os planos em que entrou: deixa de fazer parte deles.",
    kept_h="O que fica", kept_p="A lista no seu telemóvel fica até a apagar lá. Um plano em que entrou pertence a quem o criou, por isso o que acrescentou continua lá até essa pessoa o apagar. O Google Play guarda o seu próprio registo da compra do Pro. Não guardamos nenhuma outra cópia; depois, a Google limpa esses dados das cópias de segurança do Firebase com o tempo.",
    email_h="Sem a app", email_p="Perdeu o telemóvel ou a app não conseguiu concluir? Escreva para {email} a partir do endereço Google com que iniciou sessão e peça-nos para apagar a sua conta do Lunido. Apagamo-la, juntamente com os planos partilhados que criou, no prazo de 30 dias e respondemos quando estiver feito."),
"es": dict(
    lead="Lunido para Android no tiene anuncios, herramientas de análisis ni rastreo, y nunca vende tus datos. No necesitas cuenta: tu lista se queda en tu móvil, salvo que decidas compartirla.",
    stays_p="Tu lista, la fecha prevista de parto, lo que compraste o te regalaron, la bolsa del hospital y tus ajustes se quedan en tu móvil. Si la copia de seguridad de Android está activada, Android guarda una copia en tu cuenta de Google para que puedas pasarlo todo a un móvil nuevo. El desarrollador no tiene acceso a esa copia.",
    share_h="Compartir la lista (opcional)",
    share_p="Compartir es parte de Lunido Pro y solo funciona entre móviles Android. Para compartir una lista o unirte a ella, cada persona inicia sesión con Google. Lunido usa entonces dos servicios de Google Firebase. Firebase Authentication recibe tu nombre, tu correo electrónico, el enlace a tu foto de perfil de Google y un ID de usuario, y ve tu dirección IP para proteger el inicio de sesión contra abusos. Cloud Firestore guarda el plan compartido: el apodo del bebé, la fecha prevista de parto, el clima y la región, los nombres de los artículos, cantidades, estados, precios, el presupuesto, los regalos con el nombre de quién los dio, las notas y si quien creó el plan tiene Pro. En un móvil nuevo, inicia sesión con la misma cuenta de Google para recuperar la lista compartida.",
    access_p="Solo las personas de un plan pueden verlo o editarlo. Los códigos de invitación tienen 8 caracteres y caducan a los 7 días. Los datos viajan cifrados y Google los trata por cuenta nuestra según los términos de Firebase. Solo sirven para mantener la lista igual en los móviles de ambos: nunca para anuncios ni perfiles, y no se comparten con nadie más.",
    reminders_p="Android programa los recordatorios en tu móvil. No se nos envía nada.",
    delete_h="Borrar tus datos",
    delete_p="Los datos compartidos solo se guardan en Firebase mientras exista el plan: se borran cuando quien lo creó deja de compartirlo, usa Borrar todo o elimina su cuenta. Ajustes › Compartir la lista › Eliminar cuenta borra los planes que creaste, te saca de los planes a los que te uniste y después elimina tu cuenta. Ajustes › Borrar todo quita la lista de tu móvil. ¿No puedes usar la app? Consulta {delete_link}.",
    purchases_p="Lunido Pro es un pago único gestionado por Google Play. El desarrollador nunca recibe tus datos de pago.",
    children_p="Lunido está pensada para adultos que esperan un bebé. No recopilamos a sabiendas datos de niños.",
    delete_title="Eliminar tu cuenta",
    delete_lead="Solo tienes una cuenta de Lunido si iniciaste sesión con Google para compartir tu lista en Android. Sin cuenta, todo está en tu móvil: Ajustes › Borrar todo, o desinstalar la app, lo elimina.",
    inapp_h="En la app", inapp_p="Abre Ajustes › Compartir la lista, toca Eliminar cuenta (aparece mientras tienes la sesión iniciada) y confirma. Antes, Lunido te pide que confirmes tu cuenta de Google; si cancelas, no se elimina nada.",
    gone_h="Qué se elimina", gone_p="Tu cuenta de Lunido: el nombre, el correo electrónico, el enlace a la foto de perfil y el ID de usuario en Firebase Authentication. Los planes compartidos que creaste: el plan, todos sus artículos y regalos, y sus códigos de invitación; las personas con quienes lo compartiste vuelven a su propia lista. Los planes a los que te uniste: sales de ellos.",
    kept_h="Qué se conserva", kept_p="La lista de tu móvil se queda hasta que la borres allí. Un plan al que te uniste pertenece a quien lo creó, así que lo que añadiste sigue en él hasta que esa persona lo borre. Google Play conserva su propio registro de tu compra de Pro. No guardamos ninguna otra copia; después, Google borra esos datos de las copias de seguridad de Firebase con el tiempo.",
    email_h="Sin la app", email_p="¿Perdiste el móvil o la app no pudo terminar? Escribe a {email} desde la dirección de Google con la que iniciaste sesión y pídenos que eliminemos tu cuenta de Lunido. La eliminaremos, junto con los planes compartidos que creaste, en un plazo de 30 días y te responderemos cuando esté hecho."),
"fr": dict(
    lead="Lunido pour Android n'a ni publicité, ni outil d'analyse, ni suivi, et ne vend jamais vos données. Aucun compte n'est nécessaire : votre liste reste sur votre téléphone, sauf si vous choisissez de la partager.",
    stays_p="Votre liste, la date prévue d'accouchement, ce que vous avez acheté ou reçu, la valise de maternité et vos réglages restent sur votre téléphone. Si la sauvegarde Android est activée, Android en garde une copie dans votre compte Google pour que vous puissiez tout retrouver sur un nouveau téléphone. Le développeur n'a pas accès à cette sauvegarde.",
    share_h="Partager la liste (facultatif)",
    share_p="Le partage fait partie de Lunido Pro et ne fonctionne qu'entre téléphones Android. Pour partager une liste ou la rejoindre, chaque personne se connecte avec Google. Lunido utilise alors deux services de Google Firebase. Firebase Authentication reçoit votre nom, votre adresse e-mail, le lien de votre photo de profil Google et un identifiant utilisateur, et voit votre adresse IP pour protéger la connexion contre les abus. Cloud Firestore enregistre le plan partagé : le surnom du bébé, la date prévue d'accouchement, le climat et la région, les noms des articles, les quantités, les statuts, les prix, le budget, les cadeaux avec le nom de la personne qui les a offerts, les notes, et si la personne qui a créé le plan a Pro. Sur un nouveau téléphone, connectez-vous avec le même compte Google pour retrouver la liste partagée.",
    access_p="Seules les personnes d'un plan peuvent le consulter ou le modifier. Les codes d'invitation font 8 caractères et expirent au bout de 7 jours. Les données circulent chiffrées et Google les traite pour notre compte selon les conditions de Firebase. Elles servent uniquement à synchroniser la liste entre vos téléphones : jamais à la publicité ni au profilage, et elles ne sont partagées avec personne d'autre.",
    reminders_p="Les rappels sont programmés sur votre téléphone par Android. Rien ne nous est envoyé.",
    delete_h="Supprimer vos données",
    delete_p="Les données partagées ne restent dans Firebase que tant que le plan existe : elles sont supprimées quand la personne qui l'a créé arrête le partage, utilise Tout supprimer ou supprime son compte. Réglages › Partager la liste › Supprimer le compte supprime les plans que vous avez créés, vous retire de ceux que vous avez rejoints, puis supprime votre compte. Réglages › Tout supprimer efface la liste de votre téléphone. Vous ne pouvez pas utiliser l'app ? Consultez {delete_link}.",
    purchases_p="Lunido Pro est un achat unique géré par Google Play. Le développeur ne reçoit jamais vos informations de paiement.",
    children_p="Lunido s'adresse aux adultes qui attendent un bébé. Nous ne collectons pas sciemment de données sur des enfants.",
    delete_title="Supprimer votre compte",
    delete_lead="Vous n'avez un compte Lunido que si vous vous êtes connecté avec Google pour partager votre liste sur Android. Sans compte, tout est sur votre téléphone : Réglages › Tout supprimer, ou la désinstallation de l'app, l'efface.",
    inapp_h="Dans l'app", inapp_p="Ouvrez Réglages › Partager la liste, touchez Supprimer le compte (visible tant que vous êtes connecté) et confirmez. Lunido vous demande d'abord de confirmer votre compte Google ; si vous annulez, rien n'est supprimé.",
    gone_h="Ce qui est supprimé", gone_p="Votre compte Lunido : le nom, l'adresse e-mail, le lien de la photo de profil et l'identifiant utilisateur dans Firebase Authentication. Les plans partagés que vous avez créés : le plan, tous ses articles et cadeaux, et ses codes d'invitation ; les personnes avec qui vous partagiez retrouvent leur propre liste. Les plans que vous avez rejoints : vous en êtes retiré.",
    kept_h="Ce qui est conservé", kept_p="La liste sur votre téléphone y reste jusqu'à ce que vous l'effaciez. Un plan que vous avez rejoint appartient à la personne qui l'a créé : ce que vous y avez ajouté y reste jusqu'à ce qu'elle le supprime. Google Play conserve son propre historique de votre achat Pro. Nous ne gardons aucune autre copie ; Google efface ensuite ces données des sauvegardes de Firebase au fil du temps.",
    email_h="Sans l'app", email_p="Vous avez perdu votre téléphone ou l'app n'a pas pu terminer ? Écrivez à {email} depuis l'adresse Google avec laquelle vous vous êtes connecté et demandez-nous de supprimer votre compte Lunido. Nous le supprimerons, avec les plans partagés que vous avez créés, sous 30 jours et vous répondrons une fois que c'est fait."),
"de": dict(
    lead="Lunido für Android hat keine Werbung, keine Analyse-Tools und kein Tracking und verkauft deine Daten nie. Du brauchst kein Konto: Deine Liste bleibt auf deinem Handy, außer du teilst sie.",
    stays_p="Deine Liste, der Geburtstermin, was du gekauft oder geschenkt bekommen hast, die Kliniktasche und deine Einstellungen bleiben auf deinem Handy. Wenn die Android-Sicherung aktiv ist, legt Android eine Kopie in deinem Google-Konto ab, damit du alles auf ein neues Handy mitnehmen kannst. Der Entwickler hat auf diese Sicherung keinen Zugriff.",
    share_h="Liste teilen (optional)",
    share_p="Teilen gehört zu Lunido Pro und funktioniert nur zwischen Android-Handys. Um eine Liste zu teilen oder ihr beizutreten, meldet sich jede Person mit Google an. Lunido nutzt dann zwei Dienste von Google Firebase. Firebase Authentication erhält deinen Namen, deine E-Mail-Adresse, den Link zu deinem Google-Profilbild und eine Nutzer-ID und sieht deine IP-Adresse, um die Anmeldung vor Missbrauch zu schützen. Cloud Firestore speichert den geteilten Plan: den Spitznamen des Babys, den Geburtstermin, Klima und Region, die Namen der Artikel, Mengen, Status, Preise, das Budget, Geschenke mit dem Namen der Schenkenden, Notizen und ob die Person, die den Plan erstellt hat, Pro hat. Auf einem neuen Handy meldest du dich mit demselben Google-Konto an, um die geteilte Liste zurückzubekommen.",
    access_p="Nur die Personen in einem Plan können ihn sehen oder bearbeiten. Einladungscodes haben 8 Zeichen und laufen nach 7 Tagen ab. Die Daten werden verschlüsselt übertragen, und Google verarbeitet sie in unserem Auftrag nach den Firebase-Bedingungen. Sie dienen nur dazu, die Liste auf euren Handys gleich zu halten: nie für Werbung oder Profile, und sie werden mit niemandem sonst geteilt.",
    reminders_p="Erinnerungen plant Android auf deinem Handy. Nichts wird an uns gesendet.",
    delete_h="Deine Daten löschen",
    delete_p="Geteilte Daten bleiben nur so lange in Firebase, wie der Plan besteht: Sie werden gelöscht, wenn die Person, die ihn erstellt hat, das Teilen beendet, Alles löschen nutzt oder ihr Konto löscht. Einstellungen › Liste teilen › Konto löschen löscht die Pläne, die du erstellt hast, nimmt dich aus Plänen, denen du beigetreten bist, und löscht dann dein Konto. Einstellungen › Alles löschen entfernt die Liste von deinem Handy. Du kannst die App nicht nutzen? Siehe {delete_link}.",
    purchases_p="Lunido Pro ist ein Einmalkauf, den Google Play abwickelt. Der Entwickler erhält deine Zahlungsdaten nie.",
    children_p="Lunido richtet sich an Erwachsene, die ein Baby erwarten. Wir erheben wissentlich keine Daten von Kindern.",
    delete_title="Konto löschen",
    delete_lead="Ein Lunido-Konto hast du nur, wenn du dich mit Google angemeldet hast, um deine Liste auf Android zu teilen. Ohne Konto ist alles auf deinem Handy: Einstellungen › Alles löschen oder das Deinstallieren der App entfernt es.",
    inapp_h="In der App", inapp_p="Öffne Einstellungen › Liste teilen, tippe auf Konto löschen (sichtbar, solange du angemeldet bist) und bestätige. Lunido bittet dich vorher, dein Google-Konto zu bestätigen; wenn du abbrichst, wird nichts gelöscht.",
    gone_h="Was gelöscht wird", gone_p="Dein Lunido-Konto: Name, E-Mail-Adresse, Link zum Profilbild und Nutzer-ID in Firebase Authentication. Die geteilten Pläne, die du erstellt hast: der Plan, alle Artikel und Geschenke und die Einladungscodes; wer mit dir geteilt hat, kehrt zur eigenen Liste zurück. Pläne, denen du beigetreten bist: Du wirst daraus entfernt.",
    kept_h="Was bleibt", kept_p="Die Liste auf deinem Handy bleibt, bis du sie dort löschst. Ein Plan, dem du beigetreten bist, gehört der Person, die ihn erstellt hat; was du hinzugefügt hast, bleibt darin, bis sie ihn löscht. Google Play behält seinen eigenen Beleg über deinen Pro-Kauf. Wir behalten keine weitere Kopie; Google entfernt die Daten danach nach und nach aus den Firebase-Sicherungen.",
    email_h="Ohne die App", email_p="Handy verloren oder die App konnte nicht abschließen? Schreib an {email} von der Google-Adresse, mit der du dich angemeldet hast, und bitte uns, dein Lunido-Konto zu löschen. Wir löschen es samt den geteilten Plänen, die du erstellt hast, innerhalb von 30 Tagen und antworten, sobald es erledigt ist."),
"it": dict(
    lead="Lunido per Android non ha pubblicità, strumenti di analisi né tracciamento, e non vende mai i tuoi dati. Non serve un account: la tua lista resta sul tuo telefono, a meno che tu non scelga di condividerla.",
    stays_p="La tua lista, la data presunta del parto, ciò che hai comprato o ricevuto in regalo, la borsa per l'ospedale e le tue impostazioni restano sul tuo telefono. Se il backup di Android è attivo, Android ne conserva una copia nel tuo account Google, così puoi portare tutto su un nuovo telefono. Lo sviluppatore non ha accesso a quel backup.",
    share_h="Condividere la lista (facoltativo)",
    share_p="La condivisione fa parte di Lunido Pro e funziona solo tra telefoni Android. Per condividere una lista o unirti a una, ogni persona accede con Google. Lunido usa quindi due servizi di Google Firebase. Firebase Authentication riceve il tuo nome, il tuo indirizzo email, il link alla tua foto del profilo Google e un ID utente, e vede il tuo indirizzo IP per proteggere l'accesso dagli abusi. Cloud Firestore conserva il piano condiviso: il soprannome del bebè, la data presunta del parto, il clima e la regione, i nomi degli articoli, le quantità, gli stati, i prezzi, il budget, i regali con il nome di chi li ha fatti, le note e se chi ha creato il piano ha Pro. Su un nuovo telefono, accedi con lo stesso account Google per ritrovare la lista condivisa.",
    access_p="Solo le persone di un piano possono vederlo o modificarlo. I codici di invito hanno 8 caratteri e scadono dopo 7 giorni. I dati viaggiano cifrati e Google li tratta per nostro conto secondo i termini di Firebase. Servono solo a mantenere la lista uguale sui vostri telefoni: mai per pubblicità o profilazione, e non vengono condivisi con nessun altro.",
    reminders_p="I promemoria sono programmati da Android sul tuo telefono. Non ci viene inviato nulla.",
    delete_h="Eliminare i tuoi dati",
    delete_p="I dati condivisi restano in Firebase solo finché esiste il piano: vengono eliminati quando chi l'ha creato interrompe la condivisione, usa Elimina tutto o elimina il proprio account. Impostazioni › Condividi la lista › Elimina account elimina i piani che hai creato, ti fa uscire da quelli a cui ti sei unito e poi elimina il tuo account. Impostazioni › Elimina tutto rimuove la lista dal tuo telefono. Non riesci a usare l'app? Vedi {delete_link}.",
    purchases_p="Lunido Pro è un acquisto unico gestito da Google Play. Lo sviluppatore non riceve mai i tuoi dati di pagamento.",
    children_p="Lunido è pensata per adulti che aspettano un bambino. Non raccogliamo consapevolmente dati di bambini.",
    delete_title="Eliminare il tuo account",
    delete_lead="Hai un account Lunido solo se hai effettuato l'accesso con Google per condividere la lista su Android. Senza account, tutto è sul tuo telefono: Impostazioni › Elimina tutto, oppure disinstallare l'app, lo rimuove.",
    inapp_h="Nell'app", inapp_p="Apri Impostazioni › Condividi la lista, tocca Elimina account (compare finché hai effettuato l'accesso) e conferma. Prima Lunido ti chiede di confermare il tuo account Google; se annulli, non viene eliminato nulla.",
    gone_h="Cosa viene eliminato", gone_p="Il tuo account Lunido: il nome, l'indirizzo email, il link alla foto del profilo e l'ID utente in Firebase Authentication. I piani condivisi che hai creato: il piano, tutti i suoi articoli e regali e i codici di invito; chi condivideva con te torna alla propria lista. I piani a cui ti sei unito: ne vieni rimosso.",
    kept_h="Cosa resta", kept_p="La lista sul tuo telefono resta finché non la elimini lì. Un piano a cui ti sei unito appartiene a chi l'ha creato, quindi ciò che hai aggiunto resta finché quella persona non lo elimina. Google Play conserva la propria registrazione del tuo acquisto Pro. Non conserviamo nessun'altra copia; poi Google rimuove questi dati dai backup di Firebase nel tempo.",
    email_h="Senza l'app", email_p="Hai perso il telefono o l'app non è riuscita a completare? Scrivi a {email} dall'indirizzo Google con cui hai effettuato l'accesso e chiedici di eliminare il tuo account Lunido. Lo elimineremo, insieme ai piani condivisi che hai creato, entro 30 giorni e ti risponderemo a operazione conclusa."),
"nl": dict(
    lead="Lunido voor Android heeft geen advertenties, geen analysetools en geen tracking, en verkoopt je gegevens nooit. Je hebt geen account nodig: je lijst blijft op je telefoon, tenzij je ervoor kiest hem te delen.",
    stays_p="Je lijst, de uitgerekende datum, wat je hebt gekocht of gekregen, de vluchtkoffer en je instellingen blijven op je telefoon. Als de Android-back-up aanstaat, bewaart Android een kopie in je Google-account, zodat je alles naar een nieuwe telefoon kunt meenemen. De ontwikkelaar heeft geen toegang tot die back-up.",
    share_h="De lijst delen (optioneel)",
    share_p="Delen hoort bij Lunido Pro en werkt alleen tussen Android-telefoons. Om een lijst te delen of er lid van te worden, logt iedereen in met Google. Lunido gebruikt dan twee diensten van Google Firebase. Firebase Authentication ontvangt je naam, je e-mailadres, de link naar je Google-profielfoto en een gebruikers-ID, en ziet je IP-adres om het inloggen tegen misbruik te beschermen. Cloud Firestore bewaart het gedeelde plan: de bijnaam van de baby, de uitgerekende datum, het klimaat en de regio, de namen van de artikelen, aantallen, statussen, prijzen, het budget, cadeaus met de naam van wie ze gaf, notities en of degene die het plan maakte Pro heeft. Op een nieuwe telefoon log je in met hetzelfde Google-account om de gedeelde lijst terug te krijgen.",
    access_p="Alleen de mensen in een plan kunnen het bekijken of bewerken. Uitnodigingscodes hebben 8 tekens en verlopen na 7 dagen. De gegevens gaan versleuteld over het netwerk en Google verwerkt ze voor ons volgens de Firebase-voorwaarden. Ze dienen alleen om de lijst op jullie telefoons gelijk te houden: nooit voor advertenties of profilering, en ze worden met niemand anders gedeeld.",
    reminders_p="Herinneringen worden door Android op je telefoon ingepland. Er wordt niets naar ons gestuurd.",
    delete_h="Je gegevens verwijderen",
    delete_p="Gedeelde gegevens blijven alleen in Firebase zolang het plan bestaat: ze worden verwijderd als degene die het maakte stopt met delen, Verwijder alles gebruikt of het eigen account verwijdert. Instellingen › Lijst delen › Account verwijderen verwijdert de plannen die je hebt gemaakt, haalt je uit plannen waar je lid van werd en verwijdert daarna je account. Instellingen › Verwijder alles haalt de lijst van je telefoon. Kun je de app niet gebruiken? Zie {delete_link}.",
    purchases_p="Lunido Pro is een eenmalige aankoop die Google Play afhandelt. De ontwikkelaar ontvangt je betaalgegevens nooit.",
    children_p="Lunido is gemaakt voor volwassenen die een baby verwachten. We verzamelen niet bewust gegevens van kinderen.",
    delete_title="Je account verwijderen",
    delete_lead="Je hebt alleen een Lunido-account als je met Google bent ingelogd om je lijst op Android te delen. Zonder account staat alles op je telefoon: Instellingen › Verwijder alles, of de app verwijderen, haalt het weg.",
    inapp_h="In de app", inapp_p="Open Instellingen › Lijst delen, tik op Account verwijderen (zichtbaar zolang je bent ingelogd) en bevestig. Lunido vraagt je eerst je Google-account te bevestigen; als je annuleert, wordt er niets verwijderd.",
    gone_h="Wat wordt verwijderd", gone_p="Je Lunido-account: de naam, het e-mailadres, de link naar de profielfoto en de gebruikers-ID in Firebase Authentication. De gedeelde plannen die je hebt gemaakt: het plan, alle artikelen en cadeaus en de uitnodigingscodes; wie met je deelde, gaat terug naar de eigen lijst. Plannen waar je lid van werd: je wordt eruit verwijderd.",
    kept_h="Wat blijft", kept_p="De lijst op je telefoon blijft tot je hem daar verwijdert. Een plan waar je lid van werd, is van degene die het maakte; wat jij toevoegde, blijft erin tot die persoon het verwijdert. Google Play bewaart zijn eigen gegevens van je Pro-aankoop. Wij bewaren geen andere kopie; Google wist deze gegevens daarna mettertijd uit de back-ups van Firebase.",
    email_h="Zonder de app", email_p="Telefoon kwijt of kon de app het niet afronden? Mail naar {email} vanaf het Google-adres waarmee je inlogde en vraag ons je Lunido-account te verwijderen. We verwijderen het, samen met de gedeelde plannen die je maakte, binnen 30 dagen en laten het je weten als het klaar is."),
"ja": dict(
    lead="Android版Lunidoには広告、分析ツール、トラッキングがなく、あなたのデータを販売することもありません。アカウントは不要です。共有を選ばない限り、リストはあなたの端末に保存されます。",
    stays_p="リスト、出産予定日、購入したものやもらったもの、入院バッグ、設定は、あなたの端末に保存されます。Androidのバックアップがオンの場合、新しい端末にすべて移せるよう、AndroidがあなたのGoogleアカウントにコピーを保存します。開発者はそのバックアップにアクセスできません。",
    share_h="リストの共有（任意）",
    share_p="共有はLunido Proの機能で、Android端末どうしでのみ使えます。リストを共有したり参加したりするには、それぞれがGoogleでログインします。このときLunidoはGoogle Firebaseの2つのサービスを使います。Firebase Authenticationはあなたの名前、メールアドレス、Googleのプロフィール写真へのリンク、ユーザーIDを受け取り、不正利用からログインを守るためにIPアドレスを参照します。Cloud Firestoreは共有プランを保存します。保存されるのは、赤ちゃんのニックネーム、出産予定日、気候と地域、アイテム名、数量、状態、金額、予算、贈り主の名前つきのお祝い、メモ、プランの作成者がProかどうかです。新しい端末では、同じGoogleアカウントでログインすると共有リストが戻ります。",
    access_p="プランを閲覧・編集できるのは、そのプランのメンバーだけです。招待コードは8文字で、7日後に期限切れになります。データは暗号化されて送信され、GoogleがFirebaseの規約に基づき私たちに代わって処理します。用途は端末間でリストを同期することだけで、広告やプロファイリングには使わず、ほかの誰とも共有しません。",
    reminders_p="リマインダーはAndroidがあなたの端末上で設定します。私たちに送信されるものはありません。",
    delete_h="データの削除",
    delete_p="共有データがFirebaseに保存されるのは、プランが存在する間だけです。作成者が共有をやめるか、「すべて削除」を使うか、アカウントを削除すると消去されます。「設定 › リストを共有 › アカウントを削除」では、あなたが作成したプランを削除し、参加したプランから抜けたうえで、アカウントを削除します。「設定 › すべて削除」で端末からリストを消去できます。アプリを使えない場合は、{delete_link}のページをご覧ください。",
    purchases_p="Lunido ProはGoogle Playが処理する買い切りの購入です。開発者が支払い情報を受け取ることはありません。",
    children_p="Lunidoは赤ちゃんを迎える準備をする大人向けのアプリです。子どものデータを意図的に収集することはありません。",
    delete_title="アカウントの削除",
    delete_lead="Lunidoのアカウントがあるのは、Androidでリストを共有するためにGoogleでログインした場合だけです。アカウントがなければ、すべて端末内にあります。「設定 › すべて削除」またはアプリのアンインストールで消去されます。",
    inapp_h="アプリで削除する", inapp_p="「設定 › リストを共有」を開き、「アカウントを削除」（ログイン中に表示されます）をタップして確定してください。削除の前に、Googleアカウントの確認を求められます。キャンセルした場合は何も削除されません。",
    gone_h="削除されるもの", gone_p="Lunidoのアカウント：Firebase Authenticationにある名前、メールアドレス、プロフィール写真へのリンク、ユーザーID。あなたが作成した共有プラン：プラン本体、すべてのアイテムとお祝い、招待コード。共有していた相手は自分のリストに戻ります。あなたが参加したプラン：メンバーから外れます。",
    kept_h="残るもの", kept_p="端末内のリストは、そこで削除するまで残ります。参加したプランは作成者のものなので、あなたが追加した内容は作成者が削除するまで残ります。Google PlayはPro購入の記録を独自に保持します。私たちはほかにコピーを保持しません。その後、GoogleがFirebaseのバックアップからも順次消去します。",
    email_h="アプリを使わずに削除する", email_p="端末をなくした、またはアプリで完了できなかった場合は、ログインに使ったGoogleのアドレスから {email} にメールで、Lunidoアカウントの削除をご依頼ください。30日以内に、アカウントとあなたが作成した共有プランを削除し、完了したらご連絡します。"),
}

PAGE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{app} · {title}</title>
<link rel="icon" href="{up}icon.png">
<link rel="stylesheet" href="{up}../style.css">
</head>
<body>
<header><img src="{up}icon.png" alt="" width="88" height="88"><h1>{app}</h1><p>{title}</p></header>
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

# Renamed apps: every page of the old folder redirects to the same page in the new one, so links already out there
# (older builds, the store listing) keep working.
MOVED = {"clockable": "hourbee"}
REDIRECT = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={url}">
<link rel="canonical" href="{url}">
<title>Moved</title>
</head>
<body><p><a href="{url}">{url}</a></p></body>
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
    return render(lang, app, APPS[slug]["langs"], title, parts, other_doc, other_label)

def render(lang, app, langs, title, parts, other_doc, other_label, up="../"):
    current = ' aria-current="page"'
    links = " · ".join(f'<a href="{l}.html" lang="{l}"{current if l == lang else ""}>{LANG_NAMES[l]}</a>' for l in langs)
    return PAGE.format(lang=lang, app=esc(app), title=esc(title), body="\n".join(parts), other_doc=other_doc,
                       other_label=esc(other_label), other=esc(L[lang]["other"]), langs=links, up=up)

def build_android_page(lang, doc):
    """Lunido for Android, whose sharing goes through Firebase: lunido/android/{privacy,delete-account}/<lang>.html."""
    t, a = L[lang], ANDROID[lang]
    mail = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
    delete_link = f'<a href="../delete-account/{lang}.html">{esc(a["delete_title"])}</a>'
    parts = [f"<p class=\"muted\">{esc(t['updated'].format(date=t['date']))}</p>"]
    if doc == "privacy":
        reminders, region = EXTRA["lunido"][lang]
        parts.append(f"<p class=\"lead\">{esc(a['lead'])}</p>")
        sections = [(t["stays"], a["stays_p"]), (a["share_h"], a["share_p"]), (None, a["access_p"]),
                    (reminders[0], a["reminders_p"]), region, (a["delete_h"], a["delete_p"]),
                    (t["purchases"], a["purchases_p"]), (t["children"], a["children_p"]), (t["changes"], t["changes_p"]),
                    (t["contact"], t["contact_p"])]
        title, other_doc, other_label = f"{t['privacy']} · Android", "delete-account", a["delete_title"]
    else:
        parts.append(f"<p class=\"lead\">{esc(a['delete_lead'])}</p>")
        sections = [(a[k + "_h"], a[k + "_p"]) for k in ("inapp", "gone", "kept", "email")]
        title, other_doc, other_label = a["delete_title"], "privacy", f"{t['privacy_link']} · Android"
    for h, p in sections:
        if h:
            parts.append(f"<h2>{esc(h)}</h2>")
        parts.append(f"<p>{esc(p).replace('{email}', mail).replace('{delete_link}', delete_link)}</p>")
    return render(lang, "Lunido", APPS["lunido"]["langs"], title, parts, other_doc, other_label, up="../../")

CHOOSER = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{app}</title>
<link rel="icon" href="{up}icon.png">
<link rel="stylesheet" href="{up}../style.css">
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
<header><img src="{up}icon.png" alt="" width="88" height="88"><h1>{app}</h1></header>
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

def write_folder(d, app, langs, page, up="../"):
    d.mkdir(parents=True, exist_ok=True)
    for lang in langs:
        (d / f"{lang}.html").write_text(page(lang))
    links = "".join(f'<li><a href="{l}.html" lang="{l}">{LANG_NAMES[l]}</a></li>' for l in langs)
    (d / "index.html").write_text(CHOOSER.format(app=esc(app), langs_json=json.dumps(langs), links=links, up=up))
    return len(langs)

def main():
    cards, pages = [], 0
    for slug, info in APPS.items():
        app = info["name"]
        for doc in ("privacy", "support"):
            pages += write_folder(ROOT / slug / doc, app, info["langs"], lambda lang: build_page(slug, app, lang, doc))
        cards.append(f'<section class="app"><img src="{slug}/icon.png" alt="" width="64" height="64"><div><h2>{esc(app)}</h2>'
                     f'<p><a href="{slug}/support/">Support</a> · <a href="{slug}/privacy/">Privacy policy</a></p></div></section>')
    for doc in ("privacy", "delete-account"):
        pages += write_folder(ROOT / "lunido" / "android" / doc, "Lunido", APPS["lunido"]["langs"],
                              lambda lang: build_android_page(lang, doc), up="../../")
    (ROOT / "index.html").write_text(INDEX.format(cards="\n".join(cards), email=EMAIL))
    for old, new in MOVED.items():
        for page in (ROOT / new).rglob("*.html"):
            rel = page.relative_to(ROOT / new)
            (ROOT / old / rel).parent.mkdir(parents=True, exist_ok=True)
            (ROOT / old / rel).write_text(REDIRECT.format(url="../" * len(rel.parts) + f"{new}/{rel.as_posix()}"))
    print("built", pages, "pages")

if __name__ == "__main__":
    main()
