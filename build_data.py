import json,datetime,collections,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parent
ASOF='2026-11-05'
S=[]; A=[]; E=[]; C=[]; R=[]; excluded=[]

def source(key,title,publisher,url,day=None,author=None,access='web_consulted',scope='project'):
 sid='source_'+str(len(S)+1).zfill(4)
 S.append({'id':sid,'key':key,'title':title,'publisher':publisher,'author':author,'published_at':day,'url':url,'source_type':'primary' if access=='web_consulted' and publisher in ['EDF','RTE','Ville de Montereau-Fault-Yonne','Mairie de La Grande-Paroisse','Ville de Vernou-la-Celle-sur-Seine','InfraVia Capital Partners','James Chéron'] else 'press_or_context','consultation':'directly_consulted' if access=='web_consulted' else 'supplied_xlsx_extract','scope':scope,'accessed_at':ASOF})
 return sid
# Directly consulted institutional publications and independent media.
s={}
s['edf']=source('edf','EDF et OpCore s’engagent pour le développement d’un centre de données de grande puissance sur le site de l’ancienne centrale thermique de Montereau','EDF','https://www.edf.fr/groupe-edf/espaces-dedies/journalistes/tous-les-communiques-de-presse/edf-et-opcore-s-engagent-pour-le-developpement-d-un-centre-de-donnees-de-grande-puissance-sur-le-site-de-l-ancienne-centrale-thermique-de-montereau-vallee-de-la-seine-seine-et-marne','2025-11-17')
s['infravia']=source('infravia','OpCore et EDF s’engagent pour le développement d’un data center de grande puissance','InfraVia Capital Partners','https://infraviacapital.com/fr/opcore-et-edf-sengagent-pour-le-developpement-dun-date-center-de-grande-puissance/','2025-11-17')
s['rte']=source('rte','Raccorder une installation au RPT — sites Fast Track','RTE','https://www.services-rte.com/fr/decouvrez-nos-offres-de-service/raccorder-une-installation-au-RPT.html',None)
s['cheron']=source('cheron','EDF propose la construction d’un data center en bord de Seine — déclaration des maires','James Chéron','https://fr.linkedin.com/posts/james-ch%C3%A9ron-086000192_datacenter-montereau-num%C3%A9rique-activity-7302660747619168258-RF0E',None,author='James Chéron')
s['bulletin']=source('bulletin','Montereau 7 sur 7 n°1087 — lancement ministériel pour le data center','Ville de Montereau-Fault-Yonne','https://www.ville-montereau77.fr/app/uploads/1/2025/12/1087.pdf','2025-11-19',author='James Chéron')
s['actu_init']=source('actu_init','EDF veut transformer une ancienne centrale thermique en gigantesque centre de données','actu.fr','https://actu.fr/ile-de-france/montereau-fault-yonne_77305/seine-et-marne-edf-veut-transformer-une-ancienne-centrale-thermique-en-un-gigantesque-centre-de-donnees_62413125.html',None,access='xlsx_extract')
s['actu_1']=source('actu_1','Data center en Seine-et-Marne (1/4) : une ancienne centrale à charbon va devenir un immense centre de données','actu.fr','https://actu.fr/ile-de-france/la-grande-paroisse_77210/data-center-en-seine-et-marne-1-4-cette-ancienne-centrale-a-charbon-va-devenir-un-immense-centre-de-donnees_63485577.html',None,access='xlsx_extract')
s['actu_2']=source('actu_2','Data center en Seine-et-Marne (2/4) : une chance ou une imposture ? Deux députés s’opposent','actu.fr','https://actu.fr/societe/data-center-en-seine-et-marne-2-4-une-chance-ou-une-imposture-deux-deputes-sopposent_63494422.html',None,author='Agnès Gaudichon-Braik et Paul Varenguin',access='xlsx_extract')
s['parisien']=source('parisien','Seine-et-Marne : le site de l’ex centrale thermique au charbon d’EDF va accueillir un data center','Le Parisien','https://www.leparisien.fr/seine-et-marne-77/seine-et-marne-le-site-de-lex-centrale-thermique-au-charbon-dedf-va-accueillir-un-data-center-17-11-2025-NSZ57MQXGBASPEVCM4DVJOGBK4.php','2025-11-17',author='Sophie Bordier',access='xlsx_extract')
s['reuters']=source('reuters','EDF and OpCore to develop 4-billion-euro data centre in France','Reuters','https://www.reuters.com/business/energy/edf-opcore-develop-4-billion-euros-data-centre-france-2025-11-17/','2025-11-17')
s['next_2025']=source('next_2025','OpCore et EDF négocient un datacenter à 4 milliards d’euros en Seine-et-Marne','Next','https://next.ink/209358/opcore-et-edf-negocient-un-datacenter-a-4-milliards-deuros-en-seine-et-marne/','2025-11-18',author='Alexandre Laurent')
s['next_march']=source('next_march','Datacenters : EDF propose trois sites en Seine-et-Marne et en Moselle','Next','https://next.ink/brief-article/datacenters-edf-propose-trois-sites-en-seine-et-marne-et-en-moselle/','2025-03-05',author='Alexandre Laurent')
s['industrie']=source('industrie','Choose France : OpCore veut créer un datacenter sur le site d’une ancienne centrale EDF','L’Usine Nouvelle','https://www.usinenouvelle.com/article/choose-france-opcore-veut-creer-un-datacenter-sur-le-site-d-une-ancienne-centrale-thermique-edf-en-seine-et-marne.N2241484','2025-11-17',author='Patrick Désavie')
s['evasion']=source('evasion','Un projet de centre de données sur le territoire de Montereau-Fault-Yonne','Évasion FM','https://www.evasionfm.com/un-projet-de-centre-de-donnees-sur-le-territoire-de-montereau-fault-yonne','2025-03-05')
s['mesinfos']=source('mesinfos','Un projet de centre de données lancé près de Montereau-Fault-Yonne','MesInfos','https://mesinfos.fr/77130-la-grande-paroisse/un-projet-de-centre-de-donnees-lance-pres-de-montereau-fault-yonne-218488.html',None,access='xlsx_extract')
s['mairie_gp']=source('mairie_gp','Liste des élus et fonctions — La Grande-Paroisse','Mairie de La Grande-Paroisse','https://www.mairie-la-grande-paroisse.fr/fr/tb/2128817/liste-des-elus-et-fonctions',None)
s['mairie_vernou']=source('mairie_vernou','Les élus — Vernou-la-Celle-sur-Seine','Ville de Vernou-la-Celle-sur-Seine','https://www.mairie-vernou-celle77.fr/les-elus',None)
s['mairie_m']=source('mairie_m','Les élus de Montereau-Fault-Yonne','Ville de Montereau-Fault-Yonne','https://www.ville-montereau77.fr/ma-ville/conseil-municipal/les-elus/',None)
s['ccpm']=source('ccpm','Conseil communautaire du Pays de Montereau','Communauté de communes du Pays de Montereau','https://paysdemontereau77.fr/la-communaute-de-commune/les-elus/',None)
s['ccmsl']=source('ccmsl','Alain Momon — Conseil communautaire','Communauté de communes Moret Seine et Loing','https://www.ccmsl.fr/liseelusmsl/Alain-MOMON.html',None)
s['dcd']=source('dcd','EDF calls for expressions of interest from data center developers for three sites','Data Center Dynamics','https://www.datacenterdynamics.com/en/news/edf-calls-for-expressions-of-interest-from-data-center-developers-for-three-sites/','2025-03-05')
s['score']=source('score','OpCore La Grande-Paroisse — fiche de vigilance au 15 octobre 2026','Score My Data Center','https://scoremydatacenter.org/fr/dc/fr-opcore/','2026-10-15',scope='independent_assessment')
# Indexed workbook passages still source-linked, never presented as full website consultation.

def evidence(source_key, fact, location, quote=None, status='confirmed_or_attributed', date=None):
 eid='evidence_'+str(len(E)+1).zfill(4)
 E.append({'id':eid,'type':'exact_quote' if quote else 'reported_summary','text':quote if quote else fact,'summary':fact,'source_id':s[source_key],'source_status':'qualified','source_location':location,'published_at':date or next((z['published_at'] for z in S if z['id']==s[source_key]),None),'accessed_at':ASOF,'status':status})
 return eid

def actor(key,name,cat,type='organization',description='',role='',show=True):
 id=('project_montereau' if key=='PROJECT' else 'actor_'+str(len(A)).zfill(4))
 A.append({'id':id,'type':type,'name':name,'short_name':name if len(name)<30 else name[:27]+'…','description':description,'roles':[{'label':role or cat}],'categories':[cat] if isinstance(cat,str) else cat,'display_in_cards':show,'updated_at':ASOF,'slug':key})
 return id

a={}
a['PROJECT']=actor('PROJECT','Data center EDF–OpCore — Montereau-Vallée-de-la-Seine','project','project','Projet de data center de plusieurs centaines de MW annoncé en novembre 2025. OpCore et EDF ont ouvert des négociations exclusives. Implantation à Vernou-la-Celle-sur-Seine et La Grande-Paroisse.','Projet central',False)
a['site']=actor('site','Ancienne centrale thermique EDF — Montereau','project','site','Terrain industriel anciennement affecté à une centrale au charbon puis au fioul, arrêtée en 2004 et démantelée en 2011 ; 20,6 ha proposés en mars 2025.','Foncier industriel',False)
a['vernou']=actor('vernou','Vernou-la-Celle-sur-Seine','territoire','territory','L’une des deux communes physiquement concernées par le site EDF de Montereau.','Commune d’implantation',False)
a['grande']=actor('grande','La Grande-Paroisse','territoire','territory','L’une des deux communes physiquement concernées par le site EDF de Montereau.','Commune d’implantation',False)
a['montereau']=actor('montereau','Montereau-Fault-Yonne','territoire','territory','Commune voisine dont le nom désigne historiquement la centrale, mais qui n’héberge pas le foncier du projet.','Commune du bassin d’emploi',False)
a['EDF']=actor('EDF','EDF','porteurs','organization','Propriétaire du foncier industriel ; organise l’AMI de mars 2025 et engage des négociations exclusives avec OpCore en novembre 2025.','Foncier et accompagnement électrique')
a['Opcore']=actor('Opcore','OpCore','porteurs','organization','Coentreprise du groupe iliad et de fonds gérés par InfraVia ; opérateur présélectionné pour développer le futur data center.','Porteur opérationnel')
a['iliad']=actor('iliad','Groupe iliad','porteurs','organization','Actionnaire de la coentreprise OpCore, en association avec des fonds gérés par InfraVia.','Coentreprise / investisseur')
a['InfraVia']=actor('InfraVia','InfraVia Capital Partners','porteurs','organization','Gestionnaire de fonds investisseurs dans OpCore, via la coentreprise avec iliad.','Coentreprise / fonds')
a['RTE']=actor('RTE','RTE','energie','organization','Gestionnaire du réseau électrique de transport et du mécanisme de raccordement Fast Track auquel le site de Montereau est éligible.','Raccordement très haute tension')
a['CRE']=actor('CRE','Commission de régulation de l’énergie','energie','institution','Autorité de régulation ayant approuvé en 2025 le cadre du raccordement Fast Track ; cela ne constitue pas un permis accordé au data center.','Régulation du dispositif',False)
a['Etat']=actor('Etat','État français','etat','institution','Pilote la stratégie d’attractivité des centres de calcul et le cadre Fast Track ; soutien politique documenté au projet annoncé en 2025.','Soutien national')
a['Fontana']=actor('Fontana','Bernard Fontana','porteurs','person','PDG d’EDF, promoteur du recours au patrimoine industriel et à l’électricité bas carbone dans le partenariat avec OpCore.','PDG d’EDF')
a['Reynaud']=actor('Reynaud','Thomas Reynaud','porteurs','person','Directeur général du groupe iliad, soutenant la construction d’un grand centre de calcul pour l’IA et la souveraineté numérique.','Directeur général du groupe iliad')
a['Levita']=actor('Levita','Vincent Levita','porteurs','person','Fondateur et président d’InfraVia Capital Partners, se prononçant favorablement sur l’accord annoncé avec EDF.','Fondateur / président InfraVia')
a['Bermingham']=actor('Bermingham','Arnaud de Bermingham','porteurs','person','Président d’OpCore, évoque les dispositifs environnementaux et les modalités techniques à l’étude lors de l’annonce locale.','Président d’OpCore')
a['LeHenanff']=actor('LeHenanff','Anne Le Hénanff','etat','person','Ministre déléguée à l’IA et au numérique lors de l’annonce de novembre 2025, soutien politique explicite au partenariat EDF–OpCore.','Soutien ministériel en 2025')
a['Lescure']=actor('Lescure','Roland Lescure','etat','person','Ministre de l’Économie lors de l’annonce du 17 novembre 2025, défendant l’investissement et les emplois attendus.','Soutien ministériel en 2025')
a['Cheron']=actor('Cheron','James Chéron','elus-fav','person','Maire de Montereau-Fault-Yonne et président de la CC du Pays de Montereau ; favorable sous conditions d’emploi, concertation et intégration environnementale.','Maire de Montereau / président CCPM')
a['Ledoux']=actor('Ledoux','Emmanuel Ledoux','elus-fav','person','Maire de La Grande-Paroisse, favorable à la reconversion de la friche en demandant un bénéfice pour l’emploi local et une concertation transparente.','Maire de La Grande-Paroisse')
a['Momon']=actor('Momon','Alain Momon','elus-fav','person','Maire de Vernou-la-Celle-sur-Seine, défend le principe de réhabilitation industrielle en soulignant notamment l’emploi et une utilisation possible de chaleur fatale.','Maire de Vernou-la-Celle-sur-Seine')
a['Thierot']=actor('Thierot','Jean-Louis Thiériot','elus-fav','person','Député de Seine-et-Marne favorable aux centres de données, avec des déclarations sur le site de Vernou ; ses affirmations sur l’eau et les emplois restent attribuées.','Député / soutien déclaré')
a['SaintMartin']=actor('SaintMartin','Arnaud Saint-Martin','analystes','person','Député de Seine-et-Marne formulant des critiques générales sur les data centers et Fouju, tout en considérant favorablement la réutilisation d’une friche ; pas d’opposition directe établie à Montereau.','Député / position nuancée')
a['villeM']=actor('villeM','Ville de Montereau-Fault-Yonne','elus-fav','institution','Municipalité voisine participant aux échanges territoriaux et relayant le projet dans son bulletin municipal.','Collectivité associée')
a['villeGP']=actor('villeGP','Commune de La Grande-Paroisse','elus-fav','institution','Collectivité sur laquelle s’étend une partie du terrain d’implantation ; le maire s’est exprimé sur l’emploi et l’insertion.','Collectivité hôte')
a['villeV']=actor('villeV','Commune de Vernou-la-Celle-sur-Seine','elus-fav','institution','Collectivité sur laquelle s’étend une partie du terrain ; les élus ont exprimé des exigences sociales et environnementales.','Collectivité hôte')
a['CCPM']=actor('CCPM','Communauté de communes du Pays de Montereau','orgs','institution','Intercommunalité présidée en 2026 par James Chéron, en lien avec le territoire de Montereau et La Grande-Paroisse.','Intercommunalité',False)
a['CCMSL']=actor('CCMSL','Communauté de communes Moret Seine et Loing','orgs','institution','Intercommunalité de Vernou-la-Celle-sur-Seine ; Alain Momon y exerce des responsabilités, sans accord spécifique connu sur le data center.','Intercommunalité',False)
a['EDF_Lab']=actor('EDF_Lab','EDF Lab Les Renardières','formation','institution','Centre de recherche EDF voisin cité par les élus dans une réflexion sur les futures formations ; aucun partenariat contractuel local établi.','Pôle R&D de proximité',False)
a['CampusEDU']=actor('CampusEDU','Campus d’excellence Énergie Durable','formation','initiative','Programme de formation du territoire cité comme piste d’articulation avec l’emploi ; aucune convention formalisée avec OpCore établie.','Formation envisagée',False)
a['media_actu']=actor('media_actu','actu.fr / La République de Seine-et-Marne','medias','media','Presse locale ayant publié plusieurs enquêtes et interviews sur le futur centre de données.','Couverture presse',False)
a['media_parisien']=actor('media_parisien','Le Parisien','medias','media','Presse ayant documenté les annonces, le calendrier, la mobilisation institutionnelle et les hypothèses d’emploi.','Couverture presse',False)
a['media_next']=actor('media_next','Next','medias','media','Média du numérique ayant détaillé l’AMI et les négociations EDF–OpCore.','Couverture presse',False)
a['theme_grid']=actor('theme_grid','Capacité électrique et raccordement','vigilance','issue','Distinction indispensable entre plusieurs centaines de MW envisagées, capacités Fast Track, raccordement contractuel et alimentation réellement livrée.','Point de vigilance',False)
a['theme_water']=actor('theme_water','Eau et refroidissement','vigilance','issue','Promesse de refroidissement en circuit fermé relayée dans la presse ; spécifications de consommation vérifiées indisponibles.','Point de vigilance',False)
a['theme_heat']=actor('theme_heat','Chaleur fatale et usages locaux','vigilance','issue','Hypothèse de récupération de chaleur pour équipements publics, notamment piscine de Vernou, sans projet technique signé identifié.','Point de vigilance',False)
a['theme_jobs']=actor('theme_jobs','Emploi local et clauses d’insertion','vigilance','issue','Cent emplois directs évoqués par les élus, plusieurs centaines directs et indirects selon EDF ; chiffres annoncés, non constatés.','Point de vigilance',False)
a['theme_dialogue']=actor('theme_dialogue','Dialogue public et transparence','vigilance','issue','Demandes explicites de concertation et de présentation du projet aux habitants ; tenue effective des réunions non systématiquement établie.','Point de vigilance',False)
a['theme_land']=actor('theme_land','Foncier et nuisances','vigilance','issue','Site industriel de 20,6 ha proposé à l’AMI ; études détaillées d’impacts sonores et paysagers non disponibles dans ce lot.','Point de vigilance',False)
a['theme_road']=actor('theme_road','Logistique fluviale envisagée','vigilance','issue','Intention communiquée par le maire de Montereau de privilégier le transport par la Seine pour les éléments de construction.','Projet non contractualisé',False)
a['theme_timing']=actor('theme_timing','Calendrier et autorisations','vigilance','issue','Une première mise en service était annoncée pour 2027, tandis que seul le stade de négociations exclusives est confirmé par le communiqué de novembre 2025.','Point de vigilance',False)
a['theme_sovereignty']=actor('theme_sovereignty','Souveraineté numérique et IA','vigilance','issue','Argument avancé par les porteurs et l’État ; la localisation des installations ne prouve pas à elle seule la souveraineté juridique des données.','Argument politique et stratégique',False)

# Authored facts and attributed declarations. Quotes are short, user-supplied long texts are only summarized.
f={}
f['announcement']=evidence('edf','EDF et OpCore ont annoncé le 17 novembre 2025 l’ouverture de négociations exclusives pour un data center de grande puissance.','Premiers paragraphes du communiqué EDF')
f['site']=evidence('edf','Le projet est situé sur les communes de Vernou-la-Celle-sur-Seine et La Grande-Paroisse, sur l’ancienne centrale de Montereau.','Introduction / localisation')
f['investment']=evidence('edf','OpCore annonce un investissement d’environ 4 milliards d’euros, montant prospectif.','Premier paragraphe')
f['power']=evidence('edf','Le centre est présenté comme ayant une capacité de plusieurs centaines de mégawatts, sans chiffre unique définitif.','Section centre de calcul')
f['closing']=evidence('edf','La centrale au charbon de Montereau a été définitivement arrêtée en 2004.','Section réhabilitation')
f['jobs']=evidence('edf','EDF annonce plusieurs centaines d’emplois locaux directs et indirects, sans décompte réalisé.','Section calendrier et emplois')
f['timeline']=evidence('edf','Une première mise en service était envisagée pour 2027 lors de l’annonce de novembre 2025.','Section calendrier')
f['shareholders']=evidence('edf','OpCore réunit le groupe iliad et des fonds gérés par InfraVia Capital Partners.','Introduction')
f['land']=evidence('cheron','Le terrain de 20,6 ha proposé en mars 2025 appartient à EDF, avec projet de bail à construction ; cette superficie est celle du foncier proposé, pas une emprise finale bâtie.','Publication de James Chéron, paragraphes 1-2')
f['ami']=evidence('edf','La sélection fait suite à l’appel à manifestation d’intérêt d’EDF lancé le 3 mars 2025.','Section stratégie EDF')
f['grid']=evidence('rte','RTE classe Montereau parmi les sites Fast Track initialement officialisés en mai 2025 ; ce statut ne prouve pas une mise sous tension effective.','Section sites Fast Track')
f['grid_terms']=evidence('rte','La procédure Fast Track prévoit des étapes distinctes : capacité préréservée, sélection du candidat, engagement puis autorisations et raccordement effectif.','Sections 1-3 Fast Track')
f['cre']=evidence('rte','La CRE a approuvé en 2025 le cadre du dispositif Fast Track, distinct des autorisations propres au projet OpCore.','Section conditions économiques du raccordement')
f['env_target']=evidence('edf','EDF et OpCore affichent des objectifs de sobriété énergétique, optimisation de flux et économie circulaire : il s’agit d’engagements prospectifs.','Section exemplarité environnementale')
f['edf_fontana']=evidence('edf','Bernard Fontana soutient explicitement la reconversion d’une friche électrique pour accueillir un data center.','Déclaration Bernard Fontana')
f['iliad_reynaud']=evidence('edf','Thomas Reynaud soutient le projet Montereau au nom du groupe iliad pour les capacités IA et la souveraineté européenne.','Déclaration Thomas Reynaud')
f['infravia_levita']=evidence('edf','Vincent Levita salue le partenariat EDF–OpCore et la disponibilité d’électricité bas carbone.','Déclaration Vincent Levita')
f['state_lescure']=evidence('edf','Roland Lescure soutient publiquement l’investissement annoncé et ses retombées pour la réindustrialisation.','Déclaration Roland Lescure')
f['state_anne']=evidence('edf','Anne Le Hénanff salue explicitement les 4 Md€ annoncés et le projet de grande puissance à Montereau.','Déclaration Anne Le Hénanff')
f['maires_joint']=evidence('cheron','En mars 2025, James Chéron, Emmanuel Ledoux et Alain Momon demandent concertation, intégration environnementale et emplois locaux.','Publication conjointe des trois maires')
f['cheron_position']=evidence('bulletin','James Chéron réaffirme le soutien conditionnel des trois maires et évoque 100 emplois directs, transport fluvial des éléments constructifs et chaleur valorisable.','Montereau 7 sur 7 n°1087, page 1')
f['cheron_role']=evidence('mairie_m','James Chéron figure comme maire de Montereau-Fault-Yonne.','Page élus')
f['cheron_ccpm']=evidence('ccpm','James Chéron est président de la Communauté de communes du Pays de Montereau.','Conseil communautaire / président')
f['ledoux_role']=evidence('mairie_gp','Emmanuel Ledoux figure comme maire de La Grande-Paroisse.','Liste des élus et fonctions')
f['momon_role']=evidence('mairie_vernou','Alain Momon figure comme maire de Vernou-la-Celle-sur-Seine.','Liste des élus')
f['momon_ccmsl']=evidence('ccmsl','Alain Momon exerce une vice-présidence à la communauté de communes Moret Seine et Loing.','Fiche Alain Momon')
f['ledoux_support']=evidence('actu_init','Emmanuel Ledoux est favorable à la reconversion industrielle et aux recrutements locaux ; ce sont ses propos rapportés au printemps 2025.','Article actu.fr mars 2025, déclaration du maire',status='attributed_xlsx')
f['momon_heat']=evidence('parisien','Alain Momon souhaite étudier une valorisation de la chaleur pour la piscine et d’autres bâtiments publics, sans décision finale documentée.','Article Le Parisien 17 novembre 2025, propos du maire',status='attributed_xlsx')
f['momon_nuisance']=evidence('actu_init','Alain Momon estime que le remplacement d’une activité de granulats pourrait réduire le trafic routier ; bénéfice avancé, non mesuré.','Article actu.fr mars 2025, déclaration attribuée',status='attributed_xlsx')
f['bermingham']=evidence('parisien','Arnaud de Bermingham, président d’OpCore, évoque la réglementation environnementale, le refroidissement et les limites de hauteur comme éléments annoncés, non encore vérifiés en exploitation.','Article Le Parisien 17 novembre 2025, propos du dirigeant',status='attributed_xlsx')
f['water_claim']=evidence('parisien','La presse rapporte une conception censée limiter les prélèvements d’eau, mais aucun bilan hydrique opérationnel du site n’est disponible dans ce corpus.','Article Le Parisien novembre 2025, partie environnement',status='attributed_xlsx')
f['heat']=evidence('bulletin','La municipalité de Montereau évoque la distribution locale de l’énergie fatale comme objectif du projet, sans convention de livraison documentée.','Montereau 7 sur 7 n°1087, page 1')
f['river']=evidence('bulletin','La Ville souhaite que la phase chantier utilise le transport fluvial sur la Seine ; aucun marché logistique identifié dans le corpus.','Montereau 7 sur 7 n°1087, page 1')
f['education']=evidence('cheron','Les élus proposent d’articuler le projet avec EDF Lab Les Renardières, des campus de formation et les compétences locales, sans partenariat acté.','Publication James Chéron, volet formation')
f['thierot']=evidence('actu_2','Jean-Louis Thiériot se prononce favorablement aux data centers de Seine-et-Marne et au site de Vernou dans une interview locale, tout en avançant des projections et appréciations non vérifiées.','Interview croisée, réponses J.-L. Thiériot',status='attributed_xlsx')
f['saintmartin']=evidence('actu_2','Arnaud Saint-Martin exprime des critiques générales sur les impacts et emplois des très grands data centers, notamment Fouju, mais estime pertinente la réutilisation d’une friche. Pas d’opposition personnelle documentée à Montereau.','Interview croisée, réponses A. Saint-Martin',status='attributed_xlsx')
f['directjobs']=evidence('bulletin','James Chéron évoque 100 emplois directs attendus ; chiffre prospectif plus restreint que la mention EDF de plusieurs centaines de directs et indirects.','Montereau 7 sur 7, page 1')
f['sitelaw']=evidence('rte','RTE rappelle que la labellisation Fast Track ne remplace pas les autorisations environnementales et que les travaux viennent après l’engagement de raccordement.','Raccordement sur site Fast Track, sections 2-3')
f['competing']=evidence('actu_2','L’interview compare Montereau/Vernou et Fouju : les porteurs et effets ne doivent pas être fusionnés.','Introduction et questions comparatives',status='attributed_xlsx')
f['mediaactu']=evidence('actu_1','actu.fr a consacré une série au nouveau centre de calcul sur le site de l’ancienne centrale thermique.','Article 1/4')
f['mediaparisien']=evidence('parisien','Le Parisien a couvert l’annonce EDF/OpCore et interrogé les élus du territoire.','Article du 17 novembre 2025',status='attributed_xlsx')
f['medianext']=evidence('next_2025','Next a documenté la négociation annoncée entre EDF et OpCore et le passage de l’AMI à cette phase.','Article du 18 novembre 2025')
f['constructionheight']=evidence('parisien','Un projet de bâtiment limité à 10 mètres de hauteur est mentionné dans l’article du Parisien ; cette dimension reste un élément annoncé, pas un permis consulté.','Article Le Parisien, volet environnement',status='attributed_xlsx')
f['staleness']=evidence('reuters','Reuters confirme que le stade de négociations exclusives et la première phase projetée pour 2027 sont des annonces datées de 2025, sans démonstration d’une ouverture du site.','Dépêche Reuters 17/11/2025')

def claim(actor_key,value,summary,refs,certainty='high',since=None,status='attributed',topic='position_globale'):
 assert actor_key in a and refs
 C.append({'id':'claim_'+str(len(C)+1).zfill(4),'subject_id':a[actor_key],'project_id':a['PROJECT'],'claim_type':'position','topic':topic,'value':value,'summary':summary,'certainty':certainty,'status':status,'evidence_ids':[f[k] for k in refs],'valid_from':since,'valid_to':None,'updated_at':ASOF})

claim('EDF','favorable','Propriétaire foncier favorable à la reconversion industrielle ; a annoncé des négociations exclusives avec OpCore.',['announcement','ami','env_target'])
claim('Opcore','favorable','Porteur identifié des négociations exclusives, avec investissement d’environ 4 Md€ annoncé ; réalisation encore à confirmer.',['announcement','investment'])
claim('iliad','favorable','Groupe actionnaire d’OpCore dont le DG Thomas Reynaud soutient explicitement le projet.',['shareholders','iliad_reynaud'])
claim('InfraVia','favorable','Fonds gérés par InfraVia dans OpCore ; Vincent Levita soutient le partenariat annoncé.',['shareholders','infravia_levita'])
claim('RTE','neutral','Gestionnaire du réseau et du dispositif Fast Track ; sa mission technique n’est pas une prise de position politique et le raccordement réalisé n’est pas établi.',['grid','grid_terms'])
claim('Etat','favorable','Soutien national exprimé par les ministres lors de l’annonce, dans le cadre de la stratégie numérique et Fast Track.',['state_anne','state_lescure'])
claim('Fontana','favorable','Défend la reconversion de l’ancien site EDF et le raccordement rapide des futurs centres de calcul.',['edf_fontana'])
claim('Reynaud','favorable','Soutient explicitement le projet au titre de l’infrastructure souveraine et de l’innovation IA européenne.',['iliad_reynaud'])
claim('Levita','favorable','Se félicite du partenariat EDF–OpCore et défend l’usage d’électricité bas carbone pour le calcul intensif.',['infravia_levita'])
claim('Bermingham','favorable','Président du porteur industriel ; soutient le projet et présente des objectifs environnementaux encore prospectifs.',['bermingham'],'medium')
claim('LeHenanff','favorable','Salue expressément l’investissement annoncé de 4 Md€ et la place de Montereau dans la stratégie d’IA.',['state_anne'])
claim('Lescure','favorable','Présente l’investissement comme un facteur de réindustrialisation et de création d’emplois.',['state_lescure'])
claim('Cheron','favorable','Soutien politique conditionné au dialogue public, à l’insertion professionnelle locale et à l’intégration environnementale.',['maires_joint','cheron_position'])
claim('Ledoux','favorable','Soutient la reconversion de l’ex-centrale et insiste sur les emplois locaux et la transparence.',['maires_joint','ledoux_support'])
claim('Momon','favorable','Soutient la reconversion sous condition d’intégration territoriale ; souhaite examiner un usage communal de la chaleur récupérée.',['maires_joint','momon_heat'])
claim('Thierot','favorable','Soutien explicite aux data centers seine-et-marnais, notamment Vernou ; ses appréciations techniques ne sont pas des mesures indépendantes.',['thierot'],'medium')
claim('SaintMartin','neutral','Critique les hyperscalers et le projet distinct de Fouju, mais n’est pas identifié comme opposant au site de Montereau et juge la reconversion d’une friche plutôt pertinente.',['saintmartin'],'high')
claim('villeM','favorable','La municipalité soutient l’insertion territoriale du projet, notamment formation et transport fluvial envisagés.',['cheron_position','maires_joint'])
claim('villeGP','favorable','Commune d’accueil dont le maire a cosigné les exigences d’emploi local, de concertation et d’intégration environnementale.',['maires_joint','ledoux_role'])
claim('villeV','favorable','Commune d’accueil dont le maire a exprimé un soutien conditionnel et un intérêt pour la chaleur fatale.',['maires_joint','momon_heat'])

def relation(src,dst,kind,description,refs,certainty='high',status='documented',since=None):
 assert src in a and dst in a and refs
 R.append({'id':'relation_'+str(len(R)+1).zfill(4),'source_id':a[src],'target_id':a[dst],'type':kind,'summary':description,'certainty':certainty,'status':status,'evidence_ids':[f[k] for k in refs],'valid_from':since,'valid_to':None,'updated_at':ASOF})
relation('PROJECT','site','located_at','Implantation prévue sur l’ancien foncier industriel d’EDF.', ['site'])
relation('site','vernou','located_in','Une partie du site est située à Vernou-la-Celle-sur-Seine.', ['site'])
relation('site','grande','located_in','Une partie du site est située à La Grande-Paroisse.', ['site'])
relation('site','EDF','owned_by','EDF demeure propriétaire du terrain dans l’AMI de 2025.', ['land'])
relation('PROJECT','Opcore','developed_by','OpCore est le porteur identifié à l’issue de l’AMI, en négociations exclusives avec EDF.', ['announcement'])
relation('EDF','Opcore','negotiates_with','Négociations exclusives annoncées le 17 novembre 2025, pas un contrat définitif prouvé.', ['announcement'])
relation('Opcore','iliad','joint_venture_of','Coentreprise associant iliad et des fonds gérés par InfraVia.', ['shareholders'])
relation('Opcore','InfraVia','joint_venture_of','Coentreprise associant des fonds gérés par InfraVia et iliad.', ['shareholders'])
relation('PROJECT','RTE','grid_planning_with','Site Montereau labellisé Fast Track ; pas de mise en service du raccordement déduite.', ['grid','grid_terms'])
relation('CRE','RTE','regulates','La CRE a validé le cadre général de l’offre de raccordement Fast Track.', ['cre'])
relation('Etat','PROJECT','supports','Soutien ministériel à l’investissement OpCore annoncé en novembre 2025.', ['state_anne','state_lescure'])
relation('Fontana','EDF','works_for','Bernard Fontana est PDG d’EDF lors du communiqué.', ['edf_fontana'])
relation('Reynaud','iliad','works_for','Thomas Reynaud est directeur général du groupe iliad.', ['iliad_reynaud'])
relation('Levita','InfraVia','works_for','Vincent Levita est fondateur et président d’InfraVia.', ['infravia_levita'])
relation('Bermingham','Opcore','works_for','Arnaud de Bermingham est cité comme président d’OpCore.', ['bermingham'])
relation('LeHenanff','PROJECT','supports','Annonce ministérielle favorable au projet Montereau et à l’investissement prévu.', ['state_anne'])
relation('Lescure','PROJECT','supports','Soutien au projet comme levier d’activité numérique et industrielle.', ['state_lescure'])
relation('Cheron','villeM','represents','James Chéron est maire de Montereau-Fault-Yonne.', ['cheron_role'])
relation('Ledoux','villeGP','represents','Emmanuel Ledoux est maire de La Grande-Paroisse.', ['ledoux_role'])
relation('Momon','villeV','represents','Alain Momon est maire de Vernou-la-Celle-sur-Seine.', ['momon_role'])
relation('Cheron','CCPM','represents','James Chéron préside la CC Pays de Montereau.', ['cheron_ccpm'])
relation('Momon','CCMSL','represents','Alain Momon est vice-président de la CC Moret Seine et Loing.', ['momon_ccmsl'])
relation('villeGP','grande','represents','Collectivité de la commune d’accueil La Grande-Paroisse.', ['ledoux_role'])
relation('villeV','vernou','represents','Collectivité de la commune d’accueil Vernou-la-Celle-sur-Seine.', ['momon_role'])
relation('villeM','montereau','represents','Collectivité de Montereau-Fault-Yonne, commune voisine et éponyme.', ['cheron_role'])
relation('Cheron','PROJECT','supports','James Chéron accompagne le projet sous conditions locales affichées.', ['cheron_position'])
relation('Ledoux','PROJECT','supports','Emmanuel Ledoux soutient le principe du projet industriel et l’insertion locale.', ['maires_joint'])
relation('Momon','PROJECT','supports','Alain Momon soutient la reconversion industrielle et appelle à l’intégration environnementale.', ['maires_joint'])
relation('Thierot','PROJECT','supports','Jean-Louis Thiériot se prononce favorablement sur le futur centre de Vernou.', ['thierot'],'medium')
relation('SaintMartin','theme_land','raises_concern','Analyse critique générale des impacts des mégacentres ; propos non assimilés à une opposition locale.', ['saintmartin'],'medium')
relation('SaintMartin','theme_jobs','raises_concern','Analyse critique de l’intensité des emplois dans les grands centres de données.', ['saintmartin'],'medium')
relation('PROJECT','theme_grid','raises_issue','Puissance annoncée en centaines de MW et cadre Fast Track à distinguer du raccordement effectif.', ['power','grid_terms'])
relation('PROJECT','theme_timing','raises_issue','Mise en service 2027 : calendrier annoncé, susceptible d’évoluer, non avancement vérifié.', ['timeline','staleness'])
relation('PROJECT','theme_jobs','raises_issue','Projections d’emplois variées selon périmètre direct ou direct/indirect.', ['jobs','directjobs'])
relation('PROJECT','theme_water','raises_issue','Refroidissement en circuit fermé rapporté, sans bilan hydrique opérationnel publié.', ['water_claim'],'medium')
relation('PROJECT','theme_heat','raises_issue','Valorisation locale de chaleur envisagée, sans accord de fourniture constaté.', ['heat'])
relation('Momon','theme_heat','proposes','Le maire souhaite notamment chauffer la piscine et des bâtiments publics via chaleur récupérée.', ['momon_heat'])
relation('villeM','theme_road','proposes','Le bulletin municipal appelle à recourir au transport fluvial pour la phase chantier.', ['river'])
relation('Cheron','theme_dialogue','proposes','Exigence explicite de transparence et d’information des habitants.', ['maires_joint'])
relation('Ledoux','theme_jobs','proposes','Clause d’insertion et recrutements locaux demandés dans le cadre du projet.', ['maires_joint'])
relation('Momon','theme_land','proposes','Exigence d’insertion environnementale portée par les trois maires.', ['maires_joint'])
relation('PROJECT','theme_land','raises_issue','Projet sur une friche EDF de 20,6 ha (foncier proposé à l’AMI), pas une emprise finale certifiée.', ['land'])
relation('PROJECT','theme_sovereignty','supports_argument','Souveraineté numérique invoquée par les porteurs, sans en déduire un contrôle complet des données.', ['iliad_reynaud'])
relation('Cheron','EDF_Lab','mentions','EDF Lab Les Renardières cité comme piste de formation, pas partenaire contractuel confirmé.', ['education'],'medium')
relation('Cheron','CampusEDU','mentions','Campus d’excellence cité comme piste de compétences, sans convention prouvée.', ['education'],'medium')
relation('PROJECT','media_actu','covered_by','La presse locale a publié une série de reportages sur le projet.', ['mediaactu'])
relation('PROJECT','media_parisien','covered_by','Le Parisien a documenté l’annonce et les déclarations des élus et porteurs.', ['mediaparisien'])
relation('PROJECT','media_next','covered_by','Next a détaillé l’AMI et les négociations EDF–OpCore.', ['medianext'])

# Documentary synthesis. 'griefs' are questions / positions, not objectively established harm.
synthesis={
 'griefs':[
  {'title':'⚡ Demande électrique et raccordement','text':'La puissance annoncée reste « plusieurs centaines de MW » (EDF, novembre 2025). Le dispositif Fast Track permet une accélération sous conditions ; il n’atteste pas une capacité définitivement souscrite ni un raccordement en service.','evidence_ids':[f['power'],f['grid'],f['grid_terms']]},
  {'title':'💧 Eau et refroidissement','text':'Selon des responsables interrogés en novembre 2025, une conception à circuit fermé limiterait les prélèvements. Aucune consommation d’eau annuelle contractuelle ou mesurée pour ce site n’a été trouvée.','evidence_ids':[f['water_claim']]},
  {'title':'🏭 Réhabilitation de la friche','text':'La réutilisation d’un foncier EDF de 20,6 ha initialement proposé réduit les risques d’artificialisation agricole, mais ne remplace pas une étude d’impact sur les nouvelles emprises et nuisances.','evidence_ids':[f['land'],f['env_target']]},
  {'title':'👥 Emplois annoncés et insertion','text':'Le bulletin municipal évoque environ 100 emplois directs, tandis qu’EDF prévoit plusieurs centaines directs et indirects. Les annonces n’ont pas le même périmètre et ne sont pas des emplois créés.','evidence_ids':[f['directjobs'],f['jobs']]},
  {'title':'♨️ Valorisation locale de chaleur','text':'Le maire de Vernou et la Ville de Montereau souhaitent étudier la récupération de chaleur du futur site, notamment pour des équipements publics. Aucun accord de fourniture ni dimensionnement validé n’est identifié.','evidence_ids':[f['momon_heat'],f['heat']]},
  {'title':'🗣️ Dialogue et acceptabilité','text':'Les trois maires ont demandé un dialogue transparent avec les habitants. Aucune opposition locale structurée au seul projet Montereau n’est démontrée par le lot, mais l’absence de détection ne garantit pas un consensus.','evidence_ids':[f['maires_joint']]},
  {'title':'🚢 Transport pendant le chantier','text':'Le bulletin municipal mentionne la possibilité d’acheminer des éléments par la Seine. Il s’agit d’une orientation politique, pas d’un marché logistique signé.','evidence_ids':[f['river']]},
  {'title':'⚖️ Critiques nationales / distinction Fouju','text':'Le député Arnaud Saint-Martin s’interroge sur les coûts et usages des grands data centers, particulièrement Fouju ; il n’exprime pas d’opposition formelle à la friche de Montereau. Ne pas agréger les oppositions de Fouju au réseau de Montereau.','evidence_ids':[f['saintmartin'],f['competing']]}
 ],
 'vigilance':[
  {'title':'Stade juridique du partenariat','text':'Le communiqué EDF documente des négociations exclusives lancées le 17 novembre 2025. Aucun acte final plus récent, permis ou démarrage avéré ne ressort des sources retenues au 5 novembre 2026.','evidence_ids':[f['announcement'],f['staleness']]},
  {'title':'Calendrier 2027','text':'La première mise en service en 2027 reste une échéance annoncée en 2025, non une date contractuelle vérifiée.','evidence_ids':[f['timeline']]},
  {'title':'Puissance non figée','text':'Ne pas convertir les « plusieurs centaines de MW » en 700 MW ou 1 GW en reprenant les enveloppes générales du mécanisme Fast Track.','evidence_ids':[f['power'],f['grid_terms']]},
  {'title':'Différence foncier / bâti','text':'Les 20,6 ha renvoient au terrain proposé par EDF à l’AMI de mars 2025 et non à la surface finale des constructions.','evidence_ids':[f['land']]},
  {'title':'Hauteur et insertion paysagère','text':'Une limitation de hauteur à 10 mètres est mentionnée dans le reportage local de 2025 ; aucun permis opposable vérifié ne confirme cette hauteur définitive.','evidence_ids':[f['constructionheight']]},
  {'title':'Circulation et trafic routier','text':'Le maire de Vernou avance une possible diminution des nuisances liées à l’ancienne activité de granulats. L’effet net sur la circulation du futur chantier reste à étudier.','evidence_ids':[f['momon_nuisance']]},
  {'title':'Directs / indirects','text':'Une centaine d’emplois directs est évoquée localement ; plusieurs centaines directs et indirects par EDF : chiffres compatibles selon le périmètre, tous prospectifs.','evidence_ids':[f['directjobs'],f['jobs']]},
  {'title':'Chaleur et hydraulique','text':'Les opportunités de récupération de chaleur et les déclarations sur le refroidissement doivent être confirmées dans des dossiers techniques propres au projet.','evidence_ids':[f['heat'],f['water_claim']]},
  {'title':'Communes et responsabilités','text':'Projet situé à La Grande-Paroisse et Vernou-la-Celle-sur-Seine ; Montereau-Fault-Yonne participe au dialogue mais n’est pas le territoire foncier d’implantation.','evidence_ids':[f['site'],f['maires_joint']]},
  {'title':'Opposition non documentée localement','text':'Les critiques générales des data centers et les mobilisations de Fouju ne doivent pas être transposées à Montereau. Aucun collectif anti-projet nommément étayé n’a été retenu.','evidence_ids':[f['saintmartin'],f['competing']]},
  {'title':'Éviter les partenariats éducatifs fictifs','text':'EDF Lab Les Renardières et les campus de formation sont proposés comme écosystème potentiel, sans contractualisation prouvée avec OpCore.','evidence_ids':[f['education']]}
 ],
 'sources':[],
 'method':'Enjeux et griefs attribués aux acteurs ou formulés comme questions de vigilance ; aucune appréciation présentée comme un dommage constaté sans étude propre au site.'
}
for ss in S:
 if any(x['source_id']==ss['id'] for x in E):synthesis['sources'].append(ss['id'])
content={
 'project_status':'Négociations exclusives annoncées le 17 novembre 2025 ; état final non vérifié au 5 novembre 2026',
 'project_summary':'Projet industriel de data center OpCore sur l’ancienne centrale EDF dite de Montereau, située sur les territoires de La Grande-Paroisse et Vernou-la-Celle-sur-Seine.',
 'fact_sheet':[
  {'label':'Investissement','value':'Environ 4 milliards d’euros','qualifier':'Annonce OpCore / EDF de novembre 2025','evidence_ids':[f['investment']]},
  {'label':'Puissance','value':'Plusieurs centaines de MW','qualifier':'Puissance exacte et nature (appelée vs IT) non précisées','evidence_ids':[f['power']]},
  {'label':'Foncier initial','value':'20,6 ha','qualifier':'Emprise foncière de l’AMI de mars 2025, pas bâti autorisé','evidence_ids':[f['land']]},
  {'label':'Commune(s)','value':'Vernou-la-Celle-sur-Seine et La Grande-Paroisse','qualifier':'Montereau-Fault-Yonne est éponyme mais hors du terrain','evidence_ids':[f['site']]},
  {'label':'Emplois','value':'~100 directs, plusieurs centaines directs et indirects','qualifier':'Deux périmètres d’annonces, non réalisés','evidence_ids':[f['directjobs'],f['jobs']]},
  {'label':'Mise en service','value':'2027, première phase','qualifier':'Calendrier annoncé en 2025, non confirmé comme date réelle','evidence_ids':[f['timeline']]}
 ],
 'milestones':[
  {'date':'2004','period_precision':'year','status':'historical','title':'Arrêt définitif de la centrale à charbon','details':'Fin de l’activité thermique d’origine selon EDF.','evidence_ids':[f['closing']]},
  {'date':'2011','period_precision':'year','status':'historical','title':'Démolition de bâtiments de la centrale','details':'Requalification de la friche industrielle évoquée dans la communication des élus.','evidence_ids':[f['land']]},
  {'date':'2025-03-03','period_precision':'day','status':'completed','title':'Appel à manifestation d’intérêt EDF','details':'Sélection d’un projet numérique sur foncier EDF.','evidence_ids':[f['ami'],f['land']]},
  {'date':'2025-05','period_precision':'month','status':'completed','title':'Site labellisé Fast Track','details':'Montereau figure dans la première série de sites Fast Track.','evidence_ids':[f['grid'],f['sitelaw']]},
  {'date':'2025-11-17','period_precision':'day','status':'completed','title':'EDF–OpCore : négociations exclusives annoncées','details':'Investissement d’environ 4 Md€ et puissance de plusieurs centaines de MW.','evidence_ids':[f['announcement'],f['investment']]},
  {'date':'2027','period_precision':'year','status':'forecast','title':'Première mise en service envisagée','details':'Calendrier annoncé en 2025 et non confirmé comme réalisation au 05/11/2026.','evidence_ids':[f['timeline']]}
 ],
 'red_flags':[
  {'label':'Puissance IT','status':'unknown','description':'Aucun MW IT propre au projet confirmé.'},
  {'label':'Conventions de raccordement','status':'unknown','description':'Pas de convention signée identifiée dans les ressources.'},
  {'label':'Autorisations vs Fast Track','status':'distinct_steps','description':'La qualification Fast Track ne remplace pas les autorisations ni les travaux de raccordement ; voir preuve evidence id.'},
  {'label':'Permis et autorisations environnementales','status':'unknown','description':'Dossiers finaux non identifiés dans le corpus retenu.'},
  {'label':'Consommation hydrique','status':'unknown','description':'Aucune valeur annuelle chiffrée et confirmée.'},
  {'label':'Collectifs de mobilisation locale','status':'not_identified','description':'Pas d’opposants nommés de façon attribuable à ce seul projet.'}
 ]
}
meta={
 'id':a['PROJECT'],'title':'Cartographie territoriale — Data center EDF–OpCore • Montereau','subtitle':'Ancienne centrale thermique de Montereau-Vallée-de-la-Seine : Vernou-la-Celle-sur-Seine / La Grande-Paroisse. Négociations exclusives annoncées en 2025 ; faits, attentes et vigilances sourcés.','last_updated':ASOF,'created_at':ASOF,
 'data_notice':'Cartographie inaugurale, construite à partir de Montereau.xlsx (20 documents) et de publications publiques vérifiées. Les informations attribuées aux élus et aux porteurs restent des déclarations, pas des faits opérationnels constatés. Les articles uniquement accessibles via le classeur sont identifiés.','method_version':'1.0.0','central_project':a['PROJECT'],'baseline':'initial_creation','source_workbook_count':20,'source_workbook':'Montereau.xlsx','source_policy':'source URL obligatoire pour toute preuve publiée; une mention de projet voisin ne justifie pas de lien direct.'
}
taxonomy={
 'categories':{
  'all':{'label':'Tous','color':'#64748b'},
  'project':{'label':'Projet et foncier','color':'#25324f'},
  'porteurs':{'label':'Porteurs et investisseurs','color':'#4553a7'},
  'energie':{'label':'Électricité et régulation','color':'#8254c9'},
  'elus-fav':{'label':'Élus et communes favorables','color':'#2e73b9'},
  'etat':{'label':'État et stratégie nationale','color':'#586bb5'},
  'analystes':{'label':'Analyses et critiques générales','color':'#ae5365'},
  'orgs':{'label':'Institutions territoriales','color':'#2a9c91'},
  'territoire':{'label':'Communes et territoires','color':'#329eac'},
  'formation':{'label':'Formation et recherche','color':'#4b9b6f'},
  'vigilance':{'label':'Points de vigilance','color':'#d29234'},
  'medias':{'label':'Médias','color':'#8190a5'}
 },
 'stances':{
  'all':{'label':'Toutes positions','color':'#64748b'},
  'opposed':{'label':'Opposé au projet','color':'#d65d59'},
  'favorable':{'label':'Favorable ou soutien','color':'#3da784'},
  'neutral':{'label':'Prudent / position non établie','color':'#d4a044'}
 },
 'certainty_levels':{'high':{'label':'Haute'},'medium':{'label':'Moyenne'},'low':{'label':'Faible'}},
 'relation_types':{
  'located_at':{'label':'Implanté sur','directed':True},
  'located_in':{'label':'Situé sur le territoire de','directed':True},
  'owned_by':{'label':'Propriété foncière de','directed':True},
  'developed_by':{'label':'Développement envisagé par','directed':True},
  'negotiates_with':{'label':'Négocie avec','directed':False},
  'joint_venture_of':{'label':'Coentreprise de','directed':True},
  'grid_planning_with':{'label':'Cadre de raccordement','directed':False},
  'regulates':{'label':'Cadre de régulation','directed':True},
  'supports':{'label':'Soutien documenté','directed':True},
  'represents':{'label':'Représente / élu de','directed':True},
  'works_for':{'label':'Dirige / travaille pour','directed':True},
  'raises_concern':{'label':'Émet une critique générale','directed':True},
  'raises_issue':{'label':'Point de vigilance','directed':True},
  'proposes':{'label':'Propose / demande','directed':True},
  'supports_argument':{'label':'Argument stratégique annoncé','directed':True},
  'mentions':{'label':'Évoque sans partenariat établi','directed':True},
  'covered_by':{'label':'Couverture médiatique','directed':True}
 }
}

# Proofs not used by a claim, relation, synthesis, timeline or factsheet must not be published.
used=set()
for item in C+R: used.update(item.get('evidence_ids',[]))
for item in synthesis['griefs']+synthesis['vigilance']+content['milestones']+content['fact_sheet']: used.update(item.get('evidence_ids',[]))
E[:]=[item for item in E if item['id'] in used]

def dump(path,x):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for path,x in [('data/actors.json',A),('data/claims.json',C),('data/evidence.json',E),('data/relations.json',R),('data/sources.json',S),('data/synthesis.json',synthesis),('data/content.json',content),('data/meta.json',meta),('config/taxonomy.json',taxonomy)]:dump(path,x)
print('CREATED DATA', {p:len(x) for p,x in [('actors',A),('claims',C),('evidence',E),('relations',R),('sources',S)]})
