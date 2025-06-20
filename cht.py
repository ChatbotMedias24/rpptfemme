import streamlit as st
import openai
import streamlit as st
from dotenv import load_dotenv
import pickle
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import os
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from streamlit_chat import message  # Importez la fonction message
import toml
import docx2txt
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
import docx2txt
from dotenv import load_dotenv
if 'previous_question' not in st.session_state:
    st.session_state.previous_question = []

# Chargement de l'API Key depuis les variables d'environnement
load_dotenv(st.secrets["OPENAI_API_KEY"])

# Configuration de l'historique de la conversation
if 'previous_questions' not in st.session_state:
    st.session_state.previous_questions = []

st.markdown(
    """
    <style>

        .user-message {
            text-align: left;
            background-color: #E8F0FF;
            padding: 8px;
            border-radius: 15px 15px 15px 0;
            margin: 4px 0;
            margin-left: 10px;
            margin-right: -40px;
            color:black;
        }

        .assistant-message {
            text-align: left;
            background-color: #F0F0F0;
            padding: 8px;
            border-radius: 15px 15px 15px 0;
            margin: 4px 0;
            margin-left: -10px;
            margin-right: 10px;
            color:black;
        }

        .message-container {
            display: flex;
            align-items: center;
        }

        .message-avatar {
            font-size: 25px;
            margin-right: 20px;
            flex-shrink: 0; /* Empêcher l'avatar de rétrécir */
            display: inline-block;
            vertical-align: middle;
        }

        .message-content {
            flex-grow: 1; /* Permettre au message de prendre tout l'espace disponible */
            display: inline-block; /* Ajout de cette propriété */
}
        .message-container.user {
            justify-content: flex-end; /* Aligner à gauche pour l'utilisateur */
        }

        .message-container.assistant {
            justify-content: flex-start; /* Aligner à droite pour l'assistant */
        }
        input[type="text"] {
            background-color: #E0E0E0;
        }

        /* Style for placeholder text with bold font */
        input::placeholder {
            color: #555555; /* Gris foncé */
            font-weight: bold; /* Mettre en gras */
        }

        /* Ajouter de l'espace en blanc sous le champ de saisie */
        .input-space {
            height: 20px;
            background-color: white;
        }
        .input-space {
        margin-top: 1px;
        margin-bottom: 1px;
    }
        @keyframes dot-blink {
            0% { content: ""; }
            33% { content: "."; }
            66% { content: ".."; }
            100% { content: "..."; }
        }
        .loading-message {
        margin-top: 1;
        padding-top: 1px;
        font-size: 20px;
        font-weight: bold;
        white-space: nowrap;
        animation: dot-blink 1.5s infinite step-start;
        
        }
    
    </style>
    """,
    unsafe_allow_html=True
)
# Sidebar contents
textcontainer = st.container()
with textcontainer:
    logo_path = "medi.png"
    logoo_path = "NOTEPRESENTATION.png"
    st.sidebar.image(logo_path,width=150)
   
    
st.sidebar.subheader("Suggestions:")
questions = [
    "Donnez-moi un résumé du rapport ",
    "Quelles sont les grandes étapes de la reconnaissance des droits des femmes à l’échelle mondiale ?",
    "Quels sont les principaux engagements internationaux en faveur de l’égalité des sexes ?",      
    "Comment les droits des femmes ont-ils évolué au Maroc depuis l’indépendance ?",
    """Quelle a été la contribution des règnes successifs à l’émancipation féminine ?"""
]
# Initialisation de l'historique de la conversation dans `st.session_state`
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = StreamlitChatMessageHistory()

if 'previous_questions' not in st.session_state:
    st.session_state.previous_questions = []

# Ajouter une nouvelle question au début de la liste
def add_question(question):
    st.session_state.previous_questions.insert(0, question)
def main():
    text=r"""
    



                                                                                 
    Présentation du rapport
            L’étude "l’avenir de la femme marocaine à l’horizon 2050 : nœuds du futur et
    orientations de politiques publiques" s’est assignée pour objectif d’établir un état des
    lieux global des acquis et des insuffisances de la situation des femmes, d’explorer leur
    avenir en identifiant les nœuds du futur à l’horizon 2050, d’en cerner les enjeux et les
    défis actuels et futurs, et enfin, de proposer une feuille de route d’orientations
    stratégiques à court, moyen et long terme pour le Royaume, en vue d’ancrer une réelle
    effectivité de l’égalité entre les femmes et les hommes.

            La réflexion prospective a pour objectif d’anticiper les actions en faveur d'un
    avenir prospère pour tous, en interrogeant un futur possible et en proposant des
    politiques publiques à mettre en œuvre pour l’atteindre. L’analyse prospective de
    l’avenir des femmes englobe, aussi bien celle de l’évolution des modes de vie, des
    progrès technologiques, de l’ancrage de chaque individu de par le monde et de leur
    rapport quant à l’éducation et au travail, que les mutations dans le rapport de la femme
    avec son entourage immédiat, son activité professionnelle ou encore ses ambitions,
    pour ne citer que ces points.

            Ce rapport repose également sur une étude de benchmarking international, en
    matière d'amélioration de l’avenir des femmes, pour identifier de bonnes pratiques et
    en tirer un certain nombre d’enseignements envisageables pour l’avenir des femmes au
    Maroc.

            Cette analyse va au-delà des préjugés et des idées préconçues pour identifier les
    nœuds bloquants, souligner les germes de changement pouvant éclairer les possibles
    modifications de trajectoire et envisager les facteurs de dépassement. Pour la
    réalisation de cette étude, la logique méthodologique s’appuie sur une approche
    systémique et participative d’une part et sur l’usage d’outils d’analyse qualitative et
    quantitative d’autre part. Elle suit la méta-méthode prospective qui se déroule en trois
    temps qui composent l’architecture du rapport. Celui-ci s’articule en trois étapes :

•   Etape 1 : « Comprendre ». Elle dresse un état des lieux exhaustif du statut des femmes
    au sein de la société, en combinant la recherche documentaire et la collecte des
    données statistiques. L’analyse de cette base informative permet de souligner les
    avancées et les insuffisances, et de déterminer les enjeux pour l'amélioration de la
    situation des femmes.

•   Etape 2 : « Anticiper ». Elle permet d’affiner les enjeux du futur et de déterminer les
    nœuds à dépasser. L’analyse de l’évolution de ces derniers permet de construire deux
    scénarios prospectifs à l’horizon 2050 : un scénario tendanciel et un scénario
    souhaitable. Le temps de récolte de l’action politique étant long, les deux scénarios
    proposés prennent en considération l’horizon 2030 comme levier de transformation
    structurante lié entre autres actions, à l’organisation de la coupe du monde de football.




                                               5
•   Etape 3 : « Proposer ». Elle détermine les orientations stratégiques déclinées à partir du
    scénario souhaitable, lesquelles sont accélératrices de changement, pour permettre
    l’atteinte des ambitions.

            Ainsi, la première partie, "Comprendre" présente des regards croisés sur
    l'évolution des conditions des femmes entre progrès et défis, à travers un diagnostic
    sur l’état des lieux global des acquis et des insuffisances du statut des femmes au sein
    de la société marocaine. Elle s’articule en trois chapitres distincts. Le premier chapitre,
    se consacre en premier lieu à la contextualisation de la situation de la femme au niveau
    international, avant d’aborder le sujet au niveau national dans un deuxième chapitre, à
    travers le contexte historique de l'évolution des droits des femmes au Maroc et un focus
    sur les politiques publiques et l'institutionnalisation de l’égalité. Le troisième chapitre,
    quant à lui, offre un panorama diagnostic détaillé de l’état des lieux des femmes
    marocaines sous ses diverses dimensions et une analyse des enjeux à dépasser.

            La deuxième partie, "Anticiper" présente la prospective et les nœuds du futur à
    surmonter pour l'avenir des femmes à travers le quatrième chapitre qui porte sur
    l'identification et sur l'analyse de cinq nœuds du futur inhérents à la condition des
    femmes, et le cinquième chapitre qui présente les scénarios prospectifs.

          La troisième partie, "Proposer" appréhende dans le sixième chapitre le
    benchmarking international, avec un tour d'horizon des pratiques prometteuses pour
    améliorer les conditions des femmes et enfin, dans le septième chapitre, elle expose
    quelques propositions d’orientations des politiques publiques en la matière.




                                                 6
Cadrage méthodologique
        Cette réflexion repose sur un postulat essentiel : la femme est considérée dans
son environnement social, quel que soit le niveau de proximité de celui-ci à l’individu,
donc aussi bien dans son environnement intime et conjugal, que familial et sociétal.
Ainsi, le lecteur ne trouvera pas dans ce rapport de sujet exclusivement féminin, tout
simplement parce que de telles distinctions n’existent pas, tout comme il n’en existe pas
de strictement masculin.

       Cette posture implique que même les sujets culturellement envisagés comme
féminins, par exemple la contraception ou la maternité, sont considérés comme des
sujets d’intérêts également masculins, même si la contraception masculine est encore
taboue au Maroc et la paternité un sujet invisibilisé. La mise de côté de ces lunettes
"culturelles" est indispensable pour permettre de jeter un œil nouveau sur l’objet
d’étude et de réunir toutes les conditions nécessaires pour explorer le futur des femmes
marocaines en toute liberté, volonté et pouvoir, selon les trois postulats de la discipline.

        Cette précision étant établie, la méthodologie prospective adoptée vise à assurer
la clarté et la facilité d’accès. Si la complexité du sujet n’a pas été éludée, la présentation
de la réflexion a été volontairement simplifiée pour en faciliter la compréhension.

      La prospective est l’étude des futurs possibles. Il n’y a ni certitude ni hasard ou
encore moins fatalité : tout système analysé prospectivement contient des éléments de
compréhension et de construction de son avenir.

       La recherche des invariants et des tendances lourdes, et l’exploration des germes
et des leviers de changement sont autant de chances qu’il faut savoir saisir pour
impacter positivement le scénario tendanciel. S'intéresser à la place de la femme dans
le développement, et étudier les stratégies individuelles et les démarches collectives,
amène à considérer, de façon globale, les possibilités d’action, aussi bien individuelles
que collectives, des femmes dans la vie privée et publique, et conduit donc à s'interroger
sur la situation sociale de la femme. Aussi, quelle que soit sa vitesse de progrès, la
femme évolue dans un monde en mutation et ce, quel que soit l’angle et le niveau
d’analyse.

       La complexité de l’objet étudié nécessite l’adoption d’une approche systémique
d’autant plus que la femme est un acteur central de la société. En termes de logique
prospective et de manière pratique, le système étudié, ici "L’avenir des femmes au
Maroc en 2050", a été décortiqué en composantes via une analyse structurelle. Cette
dernière a été faite grâce aux diagnostics élaborés de manière bibliographique et
participative. À partir de là, chaque composante a été placée dans une carte heuristique
(Annexes) qui a permis d’identifier et de sélectionner les nœuds de blocage.




                                              7
        Afin d’affiner la réflexion, trois ateliers ont été organisés les 14, 15 et 16 février
2024 au siège de l’Institut Royal des Etudes Stratégiques, rassemblant 50 expert.e.s
chevronnés, entrepreneur.e.s, artistes, universitaires et acteurs de la société civile, dans
l’objectif d’approfondir les principaux nœuds du futur inhérents au statut de la femme
marocaine et de faire éclore des idées innovantes, dans le cadre d'une démarche
d'intelligence collective, en matière de solutions pragmatiques et susceptibles d’être
mises en œuvre, à même de promouvoir davantage l’émancipation de la femme
marocaine et de favoriser sa pleine participation au développement du pays.

       Cette démarche participative a permis de conforter le diagnostic, de prioriser les
nœuds du futur selon leur niveau d’impact sur le système et d’explorer les pistes de
solution à défricher. Ainsi, cinq nœuds leviers ont été identifiés pour articuler les deux
scénarios, tendanciel et souhaitable raisonné. Ce dernier, accélérateur de changement,
a été décliné en propositions d’orientations stratégiques, alimenté par une étude
comparative de bonnes pratiques à l’international.




                                              8
Première partie
Comprendre : regards croisés sur l'évolution des conditions des
            femmes entre progrès et défis
      Le diagnostic sur l’état des lieux global des acquis et des insuffisances du statut
des femmes au sein de la société marocaine offre un panorama détaillé de la condition
des femmes marocaines, sous ses diverses dimensions, et une analyse des enjeux à
dépasser.

Chapitre 1. Contextualisation de la situation de la femme au niveau
            international
       Au niveau international, les décennies récentes ont été marquées par des
avancées significatives dans la reconnaissance et la promotion des droits des femmes.
Cette prise de conscience mondiale quant à l'importance cruciale de l'égalité des sexes
a été déclenchée tantôt par l’adoption de programmes internationaux, tantôt par la
ratification de traités et conventions internationaux, tels que la Convention
Internationale sur l’Elimination de toutes les formes de Discrimination Raciale, la
Convention Internationale relative aux Droits de l’Enfant, ou la Convention sur
l’Elimination de toute forme de Discrimination à l’égard des Femmes, renforçant ainsi
le cadre juridique protégeant les droits fondamentaux des femmes et des filles à
l’échelle mondiale.

       Dans cette conjoncture, le dialogue international a préconisé l’intégration de
mesures concrètes visant à favoriser l’égalité entre les sexes, l’élaboration d’un cadre
juridique contraignant pour éliminer toutes les formes de discrimination à l'égard des
femmes, ainsi que la réflexion sur l’autonomisation économique des femmes, en
surmontant les obstacles entravant leur accès équitable aux ressources financières.

       Ces engagements dénotent de la volonté de positionner l'égalité entre les sexes
comme principe directeur transversal dans les politiques publiques, depuis la santé
jusqu'à l'éducation, en passant par la participation politique et l'accès au marché du
travail. À cet égard, ce chapitre s’articule en deux sections, la première étant consacrée
aux engagements mondiaux pour l’égalité entre les sexes et la seconde aux perspectives
incertaines à disposition des femmes.

1. Tracer la voie de l'égalité, des engagements mondiaux

         Au fil des décennies, la communauté internationale a pris des engagements
majeurs pour souligner l'impératif fondamental de l'égalité entre les sexes, en tant que
droit humain et socle, pour ce qui est de l'édification d'un monde pacifique, prospère et
durable. Cette section présente une analyse des actions entreprises à l'échelle
mondiale, visant à surmonter les obstacles systémiques persistants et à accélérer les
initiatives propices à la promotion de l'égalité des sexes.




                                            9
1.1.   De 1970 à 1995, une période charnière dans la lutte internationale pour les
       droits des femmes

        Les conférences mondiales sur les femmes organisées par les Nations Unies
durant les années 70 et 80 ont marqué un tournant décisif dans la prise de conscience,
par la communauté internationale, des discriminations multiples subies par les femmes
et les filles (Mexico (1975), Copenhague (1980), Nairobi (1985) et Beijing (1995)).

       Ces conférences ont été couronnées par l’adoption de programmes
internationaux, lesquels ont proclamé la nécessité de l’élaboration de politiques
destinées aux femmes pour prendre en charge les déficits existants (la Plateforme
d’action de Vienne (1993), le Programme d'Action de la Conférence internationale sur
la population et le développement (1994)).

       En 1995, la Déclaration et le Programme d’action de Beijing ont attesté le fait
que la plupart des objectifs énoncés dans les stratégies prospectives d’action de Nairobi
pour la promotion de la femme n’ont pas été atteints (1).

        Malgré les efforts déployés par les gouvernements, les effets négatifs des crises
politiques, des conflits armés et du terrorisme dans de nombreuses régions du monde
ont accentué les discriminations de fait ou systématiques, à l’encontre des femmes.
Cette période a été marquée par l’absence de protection des droits et libertés
fondamentaux de toutes les femmes et de leurs droits civils, culturels, économiques et
sociaux. Ainsi, le Programme d’action a défini des mesures à prendre à l’échelon national
et international pour la promotion de la femme à travers 12 domaines critiques (2), et
ce, en s’engageant à assurer, à titre d’exemple, de 1995 à 2000, l’accès universel à
l’enseignement, et à veiller à ce que les filles disposent des mêmes possibilités que les
garçons d’achever leurs études primaires.

       Ces programmes internationaux ont constitué une étape cruciale pour bâtir les
jalons des actions visant à éliminer les discriminations multiples et à promouvoir l'égalité
des sexes.

       Simultanément aux programmes internationaux, de multiples conventions ont
été adoptées, émettant des recommandations en faveur de la promotion de la condition
des femmes et des filles. Ces accords mettent en exergue les problèmes liés à la
discrimination raciale, reconnaissent le principe de l'intérêt supérieur de l'enfant et
adoptent un cadre juridique contraignant pour éliminer toute forme de discrimination
envers les femmes. Ce processus témoigne d'une progression chronologique des
engagements internationaux envers l'élimination des discriminations et la promotion
des droits fondamentaux, notamment, en matière de genre.




                                            10
1.2.   Vers un avenir égalitaire : des engagements mondiaux pour un développement
       durable (2000-2024)

        La Déclaration du Millénaire de 2000 a symbolisé l'engagement des dirigeants
mondiaux à lutter contre la pauvreté, l'illettrisme, la dégradation environnementale et
les discriminations envers les femmes. Selon le rapport des Objectifs du Millénaire pour
le Développement en 2015(3), ces objectifs ont permis de sortir plus d’un milliard de
personnes, y compris des femmes, de l’extrême pauvreté et de réaliser des progrès
remarquables dans la lutte contre la faim.

       Cependant, au niveau mondial, les femmes restent désavantagées sur le marché
du travail, puisque près de trois quarts des hommes en âge de travailler font partie de
la population active, contre la moitié seulement pour les femmes du même âge.

       Quinze ans plus tard, en 2015, la communauté internationale a adopté le
Programme mondial "Transformer notre monde : programme de développement
durable d'ici 2030", qui a intégré la dimension de genre de manière transversale et
consacré l’ODD 5 qui s’attache à “ parvenir à l'égalité des sexes et à autonomiser toutes
les femmes et les filles”.

       Ces engagements internationaux ont permis des avancées significatives pour la
lutte contre la pauvreté et la violence à l’égard des femmes, la promotion de l’éducation
des filles, l’accès aux droits à la santé sexuelle et reproductive, l’autonomisation
économique, ou encore l’augmentation de la participation des femmes dans la sphère
politique. Malgré les avancées réalisées, la situation internationale de ces dernières
années, fortement impactée par les répercussions de la pandémie Covid 19 et la crise
économique internationale, engendre aujourd’hui des évolutions contrastées porteuses
de craintes de régression.

2. Perspectives incertaines pour les femmes

       Au niveau mondial, les perspectives pour les femmes demeurent incertaines
malgré les avancées réalisées dans la promotion de l'égalité des sexes. Bien que des
efforts significatifs aient été déployés pour lutter contre les inégalités systémiques, des
défis persistent.

        Les femmes continuent de faire face à des disparités salariales, à des obstacles
quant à leur avancement professionnel et à des discriminations basées sur le genre. Les
réalités complexes de la vie des femmes appellent à une réflexion approfondie sur les
stratégies à adopter, qu'il s'agisse de violence de genre, d'accès inéquitable à l'éducation
ou de pressions sociales persistantes pour surmonter les obstacles restants et
construire un avenir meilleur pour les femmes et les filles.




                                              11
2.1.   Etat des lieux préoccupant pour les femmes : répercussions de la pandémie et
       défis croissants

        Malgré les avancées réalisées, les perspectives concernant les femmes, au regard
de la situation internationale de ces dernières années, sont aujourd’hui porteuses de
craintes. L’analyse des rapports des Nations Unies « Progrès vers la réalisation des
objectifs de développement durable » de 2022 (4), et de 2023 (5), met en lumière l'impact
délétère de la pandémie de la Covid-19.

       Bien que les effets de la pandémie sur les inégalités aient été globalement
compensés en termes de création d'emplois, la conjonction de cette crise avec
l'augmentation des conflits et les répercussions du changement climatique a entraîné
des conséquences négatives sur les avancées vers la réalisation de ces objectifs. Ces
constats surviennent à mi-parcours de l'échéance 2030, ce qui risque de remettre en
cause l’achèvement des objectifs si rien n’est entrepris.

        Le nombre de femmes et de filles vivant dans des contextes affectés par un conflit
est estimé à 614 millions en 2022, soit un taux supérieur de 50% par rapport à celui de
2017. En matière de réduction de la pauvreté, plus de 340 millions de femmes et de
filles sont dans l’extrême pauvreté, soit une femme sur 10. Si les tendances actuelles
demeurent inchangées, 8% de la population féminine mondiale, soit 342,4 millions,
continuera à vivre avec moins de 2,15 dollars par jour.

       L’insécurité alimentaire modérée ou grave chez les femmes adultes a augmenté
pendant la pandémie, passant de 27,5% en 2019 à 31,9% en 2021, élargissant l’écart
entre les hommes et les femmes de 1,8 à 4,3 points de pourcentage. Sans progrès
significatifs, 1 femme sur 4 sera affectée par l’insécurité alimentaire à l’horizon 2030.
De plus, les systèmes de santé, soumis à rude épreuve pendant la Covid 19, ont entraîné
des répercussions sur les femmes les plus pauvres, lesquelles se sont retrouvées privées
de soins et en mauvaise condition physique et mentale.

       Enfin, 380 millions de femmes vivent dans un contexte marqué par un stress
hydrique élevé ou critique, ce qui se répercute sur leurs conditions de vie et sur leur
santé (6).

2.2.   Défis persistants : Education, inégalités et violence à l'encontre des femmes

       Aussi, concernant l’éducation, les pertes d’apprentissage demeurent
importantes, notamment, parmi les filles marginalisées ou vulnérables. Généralement,
les progrès en matière d’éducation reculent pour les filles au niveau des cycles
supérieurs, particulièrement en termes d’opportunités d’acquisition de compétences.

       A l’échelle mondiale, 32,1% de jeunes femmes âgées de 15 à 24 ans n’étaient ni
scolarisées, ni actives, ni employées, ni en formation (Not in Education, Employment, or
Training-NEET) en 2022, contre 25,4% pour ce qui est des jeunes hommes.




                                           12
       Sans oublier la violence faite aux femmes qui a été exacerbée par les crises
sanitaires, les effets du changement climatique et les crises humanitaires. Aussi, toutes
les 11 minutes, une femme ou une fille est victime de féminicide, et une femme sur
quatre affirme que les conflits au sein des ménages sont devenus plus fréquents depuis
le début de la Covid 19.

       Le rapport 2022 de l'ONU sur la progression de l'ODD 5 soulignait que «les
dernières données disponibles sur l’ODD 5 montrent que le monde n’est pas sur la bonne
voie pour atteindre l’égalité des sexes d’ici 2030. Malgré les progrès réalisés dans la réforme
des législations, combler les lacunes dans les protections juridiques et supprimer les lois
discriminatoires pourrait prendre jusqu’à 286 ans sur la base du taux de changement actuel
» (7).

Chapitre 2 : Contexte historique de l'évolution des droits des femmes au
             Maroc et de l'émancipation féminine : une analyse à travers
             les Règnes
        L’histoire du Maroc est jalonnée de figures de femmes qui ont contribué au cours
des siècles à façonner son évolution, sans pour autant être reconnues en raison de la
culture patriarcale qui caractérise sa construction sociale. « Malgré cette organisation
sociale restrictive, les femmes ont réussi à investir la sphère publique, y compris la scène
politique, depuis les temps anciens jusqu’à nos jours » (8).

      C’est dans ce sillage historique que s’inscrit l’évolution des droits des femmes au
Maroc, fortement appuyée au cours du protectorat et depuis l’indépendance, par une
Volonté Royale affichée qui a œuvré à l’émergence de nouvelles générations de droits
des femmes tout en accompagnant leurs revendications.

       Depuis les premières initiatives jusqu'aux développements récents, des réformes
ont été entreprises pour renforcer la protection des droits des femmes, notamment,
dans les domaines du mariage et de la famille. L'accès à l'éducation a également été
encouragé, avec une attention particulière portée à l'inclusion des femmes dans le
développement socio-économique du pays.

        Le présent chapitre se penche sur l'évolution des droits des femmes à travers les
trois Règnes, en articulant cette analyse autour de quatre sections distinctes. La
première section expose la volonté Royale affirmée de bâtir une société plus équitable
et inclusive pour les femmes et les filles. La deuxième met en lumière les engagements
internationaux pris en faveur des droits des femmes, soulignant leur pertinence et leur
impact. La troisième section se concentre sur les initiatives déployées pour renforcer le
cadre institutionnel national, examinant de près les efforts entrepris pour promouvoir
l'égalité. Enfin, la quatrième section met en relief l'évolution du corpus juridique dédié
aux droits des femmes, soulignant les avancées significatives et les adaptations
juridiques qui ont marqué cette évolution au fil des Règnes successifs.




                                              13
1. Ferme volonté Royale en faveur des droits des femmes (1930- 2024)

      L'évolution de cette volonté se reflète dans les progrès significatifs réalisés au fil
des décennies, mais également dans les défis subsistants, invitant ainsi à une réflexion
continue sur les moyens d'approfondir et de consolider ces avancées pour l'avenir des
femmes.

1.1.   Feu le Sultan Mohamed V et l’éducation des femmes

        Sous le protectorat, le premier combat pour les droits des femmes a été sans
conteste celui de leur accès à l’éducation. « L’accès aux institutions scolaires fondées par
le protectorat était très limité pour les jeunes musulmanes, les écoles étant peu nombreuses
et les modalités d’obtention d’un certificat d’études primaires complexes » (9).

        En 1934, le Comité d’action marocaine, composé d’intellectuels, a élaboré un
Plan de Réformes qui comprenait, entres autres demandes, « une éducation primaire
obligatoire, moderne, et gratuite pour les enfants, garçons comme filles, âgées de 6 à 12 ans
de tous les milieux », (plan de réformes marocaines, 1934), l’éducation des femmes étant
considérée comme indissociable de la lutte pour l’indépendance. « Cette perception de
l’instruction et de l’émancipation des femmes au Maroc s’est développée simultanément au
mouvement nationaliste, et a pris une importance sans précédent dans les années 1940.
L’obtention de certificats d’études primaires par une première cohorte de filles en 1942, et
l’émergence des premiers partis politiques ont contribué à donner une portée encore plus
grande à ces mouvements » (10).

        C’est dans ce contexte que s’inscrit l’action de Feu le Sultan Mohamed V, soutien
du mouvement de libération nationale et fervent défenseur de l’éducation des filles, qui
encouragea les Marocains à suivre son exemple, à travers l’accès des filles de Sa Majesté
à l’école, telle la Princesse Lalla Aïcha. Le Discours historique de la Princesse, à visage
découvert, prononcé à Tanger le 11 avril 1947, marque un tournant décisif en affirmant
que la renaissance de la Nation ne saurait faire l’économie de l’éducation de la femme,
devenant ainsi un symbole pour son émancipation, et ouvrant la voie à l’éducation des
femmes, à leur participation croissante sur le marché du travail et à une évolution
progressive des droits des femmes, de l’indépendance jusqu’à nos jours (11).

1.2.   Feu le Roi Hassan II et les droits politiques et institutionnels

       C’est ainsi que, sous l’égide de Feu le Roi Hassan II, et dès la Constitution de
1962, des droits politiques et sociaux sont reconnus, tels que le droit de vote et de
candidature aux élections dans les mêmes conditions que l’homme, le droit de grève, la
liberté d’opinion, la liberté d’expression et de réunion ou la liberté d’association et
d’adhésion à toute organisation syndicale et politique de son choix, droits réaffirmés
depuis dans les Constitutions successives qu’a connues le Royaume.

       Certes, la construction sociale du pays, fondée sur la prédominance du système
patriarcal, n’a pas permis l’accession rapide des femmes aux postes de responsabilités
politiques et institutionnelles au cours des premières décennies de l’indépendance.




                                             14
       Sur le plan économique également, elles sont restées longtemps confinées dans
des secteurs sociaux traditionnels. Parallèlement, au niveau juridique, l’adoption en
1958 du Code du statut personnel et successoral a créé une rupture avec les synergies
positives du combat pour l’indépendance.

       Néanmoins, les profondes mutations sociologiques, l’urbanisation rapide,
l’apparition d’une élite féminine citadine, l’investissement par les femmes des espaces
publics, l’accès des femmes à l’éducation, leur entrée massive sur le marché du travail,
le début de maîtrise de leur fécondité par la diffusion des méthodes contraceptives,
etc., ont peu à peu créé les conditions du changement, relayées par la montée en
puissance du mouvement des droits des femmes.

        Les années 90 ont été ainsi marquées par des avancées sur les plans juridique et
institutionnel. La réforme du Code du statut personnel en 1993 a apporté de légères
modifications, en particulier à la tutelle matrimoniale (wilaya) et à la garde des enfants
mineur.e.s, et la polygamie est devenue conditionnée par l’octroi de l’accord de la
première femme. Par ailleurs, en juillet 1995, le Code du commerce a libéré l’exercice
des activités commerciales des femmes mariées, en abolissant l’obtention de l’accord
préalable du mari.

       Sur le plan institutionnel, les premières femmes sont élues aux communales en
1976 et deux femmes accèdent au parlement en 1993, ce qui constitue le début de leur
responsabilisation au niveau législatif et dans les bureaux des communes, sans compter
l’accès des femmes aux hauts niveaux de la hiérarchie publique, soit quatre femmes
nommées secrétaires d’État dans le Gouvernement de 1997.

       Le Maroc a aussi souscrit à la Convention sur l’élimination de toute forme de
discrimination à l’égard des femmes (1993). Des tabous relatifs à la sacralité de la
Moudawana et à l’accès des femmes au pouvoir sont ainsi levés, annonçant une
évolution positive qui se confirmera avec l’accession au Trône de Sa Majesté Le Roi
Mohammed VI.

1.3.   Sa Majesté Le Roi Mohammed VI : une forte volonté de changement

      La situation de la femme marocaine a toujours constitué l’une des
préoccupations majeures de Sa Majesté Le Roi Mohammed VI, dans la vision d’un
Maroc prospère, moderne, démocratique et développé.

       Lors du Discours du Trône du 30 juillet 2022, Sa Majesté Le Roi Mohammed VI
a rappelé que « Depuis Notre accession au Trône, Nous avons veillé à la promotion de la
condition de la femme, en lui offrant toutes les possibilités d’épanouissement et en lui
accordant la place qui lui revient de droit… De fait, la condition sine qua non pour que le
Maroc continue de progresser est qu’elles occupent la place qui leur échoit et qu’elles
apportent leur concours efficient à toutes les filières de développement ».




                                            15
       Le Royaume du Maroc a lancé, à partir des années 2000, un processus de
réformes qui se sont penchées sur les défis à relever en termes de stabilité macro-
économique, d’efficience institutionnelle, d’intégration internationale et régionale de
l’économie, de développement industriel, d’emploi des jeunes, de cohésion sociale et
de lutte contre la pauvreté, de lutte contre les violences à l’encontre des femmes et de
promotion de leurs droits.

        La Constitution de juillet 2011 est venue couronner le processus de réformes
engagées et annoncer une nouvelle ère de réformes, pour parachever la consolidation
de la démocratie au Maroc et impulser un développement humain durable et inclusif,
caractérisé par un État social fort. En consacrant l'égalité et la parité femme-homme,
dans son article 19, elle représente une étape historique de ces avancées. Elle comporte
des dispositions constitutionnelles inédites dans le monde arabo-musulman, renforcées
par des mécanismes institutionnels, et qui appellent au respect des droits humains. Il
s’agit, en particulier, de la promotion des droits des femmes et du droit à une
citoyenneté effective, en plus de l'harmonisation de l'arsenal juridique avec les
conventions internationales ratifiées par le Maroc, dans le respect des constantes
immuables de la Nation. En 2021, le nouveau modèle de développement est venu
réaffirmer cette orientation.

        Sur le plan législatif, la réforme du Code du Statut personnel et son passage au
Code de la famille est sans nul doute la plus importante réforme du début du 21 ème
siècle, annoncée par Sa Majesté le Roi Mohammed VI, le 10 octobre 2003. Même si ces
acquis font toujours l’objet de résistances sociales et culturelles qui diminuent leur
effectivité, une nouvelle annonce de leurs réformes a été faite par le Souverain, dans sa
lettre au Chef de Gouvernement le 26 septembre 2023, réaffirmant le fort engagement
au plus haut niveau de l’Etat, de poursuivre l’amélioration de la condition de la femme.

2. Engagements internationaux vigoureux en faveur des droits des femmes : une
   trajectoire déterminée

       Conscient du caractère universel et indivisible des droits de l'Homme, le
Royaume s'est engagé activement à coopérer, de façon durable, avec le système
onusien des droits humains. Cette section met en exergue l’impact des déclarations et
conventions ratifiées par le Maroc prohibant les discriminations ainsi que le
renforcement de la pratique conventionnelle.

2.1.   Adhésion aux déclarations onusiennes pour la promotion des droits
       fondamentaux : un fort engagement

        Les engagements internationaux souscrits par le Maroc ont consolidé la volonté
proclamée par le nouveau Règne dès son début, cherchant à opérer une intégration
graduelle des femmes dans les structures économiques, sociales et institutionnelles
face à la montée en puissance de la mondialisation. A cet effet, le Maroc s’est
activement impliqué dans toutes les conférences mondiales sur les femmes, et a été
signataire de plusieurs déclarations ou programmes d’actions mobilisateurs (12) (la
Déclaration du Millénaire, le Programme mondial de développement durable d'ici 2030 (13),
l'Agenda de l'Union Africaine à l’horizon 2063 (14), le Plan Mondial d'accélération de la
réalisation des droits des femmes et des filles, la Déclaration de Nairobi).

                                           16
      Sur le plan des droits de l’Homme, le Maroc a souscrit politiquement et
moralement aux différents textes du système international des droits de l’Homme et à
ses neuf principaux instruments, auxquels s’ajoute la résolution internationale n°1325
du Conseil de sécurité des Nations Unies, adoptée en 2000, et qui a été déclinée au
niveau national dans un Plan d'action national "Femmes, Paix et Sécurité", lancé en mars
2022.

       Dans cette perspective, un processus de réformes a été amorcé avec une volonté
de réduire les disparités sociales, territoriales et de genre, tout en veillant à instaurer
une démocratisation du système institutionnel de gouvernance en réponse aux
aspirations féminines.

        Des progrès significatifs ont été graduellement accomplis pour la consécration
constitutionnelle de la primauté des conventions internationales, l’adoption de
stratégies sectorielles, la valorisation du pluralisme linguistique, culturel, religieux de
l’identité marocaine, en assurant la conformité des droits humains avec les
engagements pris dans les conventions et protocoles ratifiés par les instances
compétentes des Nations Unies.

       Les acquis en matière d'égalité des droits, particulièrement dans les domaines
matrimonial, social et politique, ont été consolidés avec la levée des réserves de la
Convention sur l'élimination de toutes les formes de discrimination à l'égard des
femmes, et l’adoption de son Protocole facultatif (15). Dans cet élan, une panoplie de
stratégies a été adoptée pour promouvoir les droits des femmes et des enfants, tout en
luttant contre les violences.

2.2.   Renforcement de la pratique conventionnelle

        Pour parachever son adhésion au système international, le Royaume a
intensivement œuvré pour le renforcement de la pratique conventionnelle dans le
domaine de la protection des droits de l'Homme. Cela s'est concrétisé par une
interaction soutenue avec toutes les instances des traités, accompagnée de la
présentation régulière de rapports aux organes conventionnels (16) conformément à ses
engagements (17). En janvier 2024, le Maroc est élu à la Présidence du Conseil des Droits
de l’Homme, basé à Genève, pour une durée d'un an. En dépit des efforts déployés, il
demeure impératif de persévérer et d'intensifier les efforts visant à harmoniser les
législations nationales avec les normes internationales inhérentes aux conventions des
droits de l’Homme auxquelles le Maroc a adhéré.

3. Renforcement du cadre institutionnel national au prisme de l’égalité

       Au début du millénaire, le Maroc a placé les droits des femmes au premier plan
des réformes institutionnelles, en menant un processus de modernisation du statut des
femmes marocaines, marqué par des avancées importantes, en matière d’égalité
femme-homme, de promotion et de protection des droits des femmes, aussi bien au
niveau du cadre normatif que dans les politiques publiques, les stratégies sectorielles et
les mécanismes institutionnels.




                                            17
      Cette section abordera la constitutionnalisation du principe d'égalité et de parité,
en mettant l'accent sur le rôle structurant des institutions nationales constitutionnelles,
ainsi que l'intégration de la perspective de genre au sein des programmes
gouvernementaux.

3.1.   Constitutionnalisation de l’égalité et de la parité et lutte contre les
       discriminations

        L’adoption de la Constitution 2011 à travers le premier référendum du Règne de
Sa Majesté le Roi Mohammed VI a marqué l'histoire contemporaine du Maroc,
témoignant de la volonté de modernisation du pays. Celle-ci a été promulguée pour
répondre aux aspirations de la population marocaine en matière de réformes politiques
et démocratiques, y compris celles des femmes. Elle constitue à la fois une charte des
droits et des libertés, et un cadre juridique pour la consécration des principes de l’égalité
et de la parité, accordant une primauté du droit international. Bien qu'elle ait progressé
graduellement vers une harmonisation avec les conventions internationales ratifiées,
un retard subsiste en ce qui concerne l'alignement des lois nationales avec la
Constitution.

       Dans cet élan de réformes pour institutionnaliser l’égalité femme-homme, le
Maroc a progressivement mis en place des mécanismes institutionnels (Conseil National
des Droits de l’Homme, Conseil Economique Social et Environnemental, Haute Autorité
de la Communication Audiovisuelle, ...) qui ont accompagné la moralisation de la vie
publique, en vue de renforcer la culture démocratique fondée sur le principe de la
concertation et de donner à la démocratisation du pays une vocation participative
croissante, à travers l’émission d’avis de saisine et de mémorandums importants qui ont
contribué à l’avancement de la cause des femmes(18).

        Par ailleurs, en 2019, dans le cadre de l'intensification de la lutte contre la
violence, de nouvelles commissions ont été créées (Commission Nationale pour la Prise
en Charge des Femmes Victimes de Violence, Commission Nationale de Coordination
des Mesures de Lutte et de Prévention contre la Traite des Etres Humains (19)). Bien que
leurs attributions soient limitées et qu'elles fassent face à des contraintes budgétaires,
ces commissions s'efforcent de coordonner les efforts des différents acteurs pour
mettre en place des mécanismes améliorés de gestion des cellules d'assistance aux
femmes victimes de violence, et de renforcement de la protection des victimes de la
traite des êtres humains.

        Dans le même élan de réformes, nouvellement créée par le Gouvernement en
2022, la Commission Nationale pour l’Egalité entre les sexes et l’Autonomisation de la
Femme (20) a adopté en mars 2023, le cadre stratégique de l’égalité et de la parité à
l’horizon 2035. Ce cadre stratégique s'inscrit dans le cadre du Plan Gouvernemental
pour l'Egalité III, qui couvre la période 2023-2026. Le véritable défi de cette commission
est de suivre de près, la mise en œuvre et l'implémentation effective de ce cadre
stratégique pour répondre aux mutations sociales d'ici 2035.




                                             18
        En dépit des efforts déployés, le rapport sur les Objectifs de développement
durable de 2015 du Haut-commissariat au Plan a mis en lumière diverses contraintes
au sein du paysage institutionnel marocain, et qui freinent l'émancipation des femmes.
Ces défis sont principalement associés au retard dans la mise en œuvre des dispositions
de la Constitution visant à réduire les inégalités femmes-hommes, à l'ampleur des
perceptions sociales et des valeurs traditionnelles entravant la promotion de l'égalité
des sexes, à la faiblesse de l'implication des médias dans la promotion des valeurs
d'égalité, et à la prédominance du travail non rémunéré pour une grande partie des
femmes actives, dont la moitié a un statut d'aides familiales (21).

3.2.   Intégration progressive du genre dans les politiques publiques (1998-2010)

       L'intégration graduelle du genre dans les programmes gouvernementaux qui se
sont succédés au Maroc, témoigne d'un engagement croissant envers l'égalité des
sexes, ainsi qu'une prise de conscience de l'importance d'adresser, de manière
différenciée, les spécificités des femmes et des hommes dans toutes les sphères de la
société.

       Dans le cadre de son implication croissante dans la dynamique mondiale des
années 90, et après la ratification formelle de la CEDAW (22), le Maroc a établi, en 1998,
le Secrétariat d'État chargé de la Protection Sociale, de la Famille et de l'Enfance (23).
Dès sa création, cette institution a implémenté une approche intégrée et une
perspective d'analyse de genre dans le traitement des questions liées à l'égalité des
sexes, y compris celles liées à la violence basée sur le genre (24).

       Dans cette vision, le Secrétariat d'Etat chargé de la Protection Sociale, de la
Famille et de l'Enfance a amorcé un débat décisif dans l’Histoire du Maroc avec la
proposition du Plan d'action national d'intégration de la femme au développement, la
même année. Bien que ce plan n'ait pas été officiellement adopté, il a néanmoins généré
une dynamique socio-politique autour de la question de l’égalité de genre par une
mobilisation sans précédent de l’opinion publique, de la société civile et des décideurs
politiques.

        La promulgation du Code de la famille, le 10 octobre 2004 par Sa Majesté le Roi
Mohammed VI a conduit à une nouvelle ère qui prône l’instauration d’un nouveau droit
de la famille, lequel préconise l’égalité entre les époux, dans une responsabilité partagée
de la famille, bouleversant ainsi l’ordre établi du patriarcat et permettant la consécration
de la femme marocaine en tant que citoyenne à part entière.

3.3.   Cheminement de la protection des femmes : évolution contre la violence et les
       discriminations (2011-2021)

       Dans la dynamique de l’adoption de la Constitution de 2011, le Maroc a adopté
le premier Programme Gouvernemental de l’égalité nommé "ICRAM I" (2012-2016)
suivi du programme "ICRAM II" (2017-2021), lesquels ont constitué un cadre de
convergence pour les initiatives des divers départements ministériels, œuvrant à
intégrer l'approche genre dans l'ensemble des politiques nationales.




                                            19
          Grâce aux efforts consentis pour l’atteinte des Objectifs du Millénaire pour le
Développement, le Maroc a enregistré en 2015 des réalisations qui avoisinaient les 65%
(25) (la baisse du taux de mortalité, l'éradication de l’extrême pauvreté, la généralisation

de l’enseignement primaire).

        Cette volonté affirmée de l’Etat, alignée aux engagements internationaux
ratifiés, s’est poursuivie en ouvrant un nouveau chapitre en matière de protection des
droits des femmes, des enfants, des handicapés, et ce, avec l’adoption de nouvelles
politiques publiques en faveur de la promotion des personnes handicapées, la lutte
contre la violence (Déclaration de Marrakech en 2020, le protocole territorial du PMP en
2021), la protection de l’enfance (Plan d'action intégré de lutte contre le mariage des
mineurs en 2022 (26)), l’autonomisation des femmes (Maroc attamkine" et la Stratégie
GISSR) et l'institutionnalisation de l'égalité entre les sexes dans diverses politiques
publiques (27), y compris la fonction publique, l'emploi et la formation professionnelle,
accompagnées de mesures telles que la budgétisation sensible au genre.

        Certes, ces stratégies ont eu un impact considérable sur la criminalisation de la
violence et la mise en place de mécanismes assurant la prise en charge et la protection
des femmes (28), ainsi que la protection de l’enfance. Néanmoins, malgré les avancées
enregistrées, des contraintes (29) persistent encore, en lien avec la faiblesse de la
convergence et de la cohérence des politiques et programmes de développement sur
l’égalité, la lenteur de l’intégration de l’égalité dans certaines politiques publiques et la
faiblesse de la coordination entre les acteurs de la chaîne de prise en charge des femmes
victimes de violence.

       Comme le reste du monde, les avancées en termes de baisse de pauvreté et
d’inégalités ont été compromises, suite aux effets de la pandémie Covid-19 et des
conséquences de l’environnement international instable.

       En matière d’évolution des inégalités des niveaux de vie, la tendance baissière
des taux de pauvreté et de vulnérabilité au Maroc a été brisée par les effets combinés
de la crise sanitaire liée à la Covid-19 et du choc inflationniste, et il a été estimé par le
HCP (2023) que le pays a perdu sept années de progrès vers l’élimination de la pauvreté
et de la vulnérabilité. Environ 3,2 millions de personnes supplémentaires ont basculé
dans la pauvreté (1,15 million) ou dans la vulnérabilité (2,05 millions). Près de 45% de
cette détérioration de la pauvreté et de la vulnérabilité est due à l’effet de la pandémie
et 55% à l’effet de la hausse des prix à la consommation (30).

3.4.   Effectivité de l’égalité et développement durable : des défis sociétaux pour
       l’avenir

        Pour répondre à ces enjeux structurels pour l'accélération des Objectifs de
Développement Durable, de nouvelles stratégies à l’horizon de 2030 ont été adoptées
et alignées sur les engagements du Programme mondial de développement durable d'ici
2030 relatives à l’éducation, la Santé Sexuelle et Reproductive, le Développement
Durable 2030, l'Emploi, la protection sociale...




                                             20
        Dans la continuité de la mise en œuvre des politiques antérieures, le Programme
Gouvernemental 2021-2026 a placé l'amélioration des indicateurs économiques et
sociaux des femmes en tant que priorité. L'objectif est d'augmenter le taux d'activité
des femmes à plus de 30%, dépassant ainsi le taux actuel de 19,8 %, et de réduire les
disparités sociales et territoriales à moins de 39%, comparé à l'indice de Gini actuel de
46,4%(31). Dans cette perspective, le Plan Gouvernemental pour l'Égalité III (2023-2026)
a priorisé trois axes majeurs : l'autonomisation et le leadership, la protection et le bien-
être, ainsi que les droits et les valeurs.

       Certes, ces stratégies ont joué un rôle important dans le changement des
perceptions et contribué à fissurer les barrières sociales qui freinent la consécration de
la citoyenneté effective des femmes et qui réduisent leur accès aux droits
fondamentaux. Toutefois, en dépit de la mise en place des différentes politiques
publiques énoncées, l’effectivité de l’égalité peine encore à se concrétiser.

       Des défis subsistent quant à la pleine réalisation de l’égalité des droits au niveau
du statut personnel, à une égale participation dans la sphère politique et économique,
et les discriminations intersectionnelles demeurent prépondérantes dans les espaces,
public et privé, les femmes et les jeunes filles ne jouissant pas, dans la pratique, de tous
leurs droits. Beaucoup de discriminations subsistent encore dans l'arsenal juridique et
dans les pratiques, constituant ainsi un frein pour ce qui est de leur autonomisation.

4. Evolution du corpus juridique en faveur des droits des femmes

       L'évolution du corpus juridique en faveur des droits des femmes au Maroc a suivi
une trajectoire significative au fil des années. Plusieurs réformes législatives ont été
entreprises pour renforcer la protection des droits des femmes et promouvoir l'égalité
des sexes. Cette section présentera une analyse sur de grandes réformes législatives
entreprises pour renforcer graduellement l’élan de progrès institutionnel amorcé en
faveur des droits des femmes, tout en mettant en lumière les défis persistants.

4.1.   Réformes juridiques pour répondre aux dynamiques sociétales en constante
       mutation

       Au tournant des années 2000, le Maroc a entrepris d'importantes réformes
juridiques visant à instaurer un accès universel aux droits, assurer l'égalité entre les
individus, atténuer relativement les disparités économiques et territoriales, tout en
luttant contre les discriminations fondées sur le genre.

        Malgré ces avancées, l'évolution du statut des femmes dans la société marocaine
requiert des ajustements continus pour refléter, dans l’avenir, les dynamiques sociétales
en constante évolution. Cette vision est inscrite dans le Discours du Souverain
prononcé à l’occasion du 23ème anniversaire de la fête de Trône : « … Il convient aussi
de dépasser les défaillances et les aspects négatifs révélés par l’expérience menée sur le
terrain et, le cas échéant, de refondre certaines dispositions qui ont été détournées de leur
destination première ».




                                             21
        Certes, la réforme du Code de la famille de 2004 a apporté des changements
significatifs en influençant les pratiques quotidiennes des hommes et des femmes, tout
en contribuant à la consolidation des droits, d’autant plus lorsqu’on la compare aux
autres pays arabes dont la législation relative au statut personnel est ancrée dans la
Charia islamique. Selon l'enquête du lien social de l’IRES de 2024, 85 % des personnes
interrogées affirment que le Code de la famille a amélioré la condition des femmes, mais
seulement 58 % estiment que ce Code a été correctement appliqué (61 % des hommes
et 55 % des femmes) (32).

       Depuis son avènement, le Code de la famille a proclamé la consécration du
principe de l’égalité et de la coresponsabilité des époux dans la prise des décisions
concernant la vie familiale. Toutefois, des lacunes persistent, notamment en ce qui
concerne l'octroi de la tutelle légale exclusive au père, un principe de coparentalité en
cas de rupture conjugale, reste en contradiction avec les principes de partage des
responsabilités entre les conjoints, et en ce qui concerne les enfants (la gestion des
intérêts patrimoniaux, la scolarisation, les allocations familiales et l’assurance maladie,
le voyage à l’étranger). En outre, la femme est déchue de la garde en cas de remariage,
une situation qui diffère de celle du père.

       Le Code de la famille a introduit une mesure cruciale en soumettant la
dissolution du lien matrimonial à la décision du tribunal, plutôt qu'à l'initiative
unilatérale de l'époux, tout en maintenant un contrôle judiciaire. De nouvelles modalités
de divorce ont été instaurées à l’époque, notamment, le divorce par consentement
mutuel et le divorce pour discorde « Chiqaq », ce type de divorce a atteint 99,1%, en
2022, selon le rapport du HCP (33) de 2023. Néanmoins, il est important de souligner
que l’absence de définition juridique claire du divorce par discorde pose un défi réel, en
termes de détermination des critères nécessaires pour justifier le prononcé du divorce.

        Selon le rapport des indicateurs sociaux du HCP de 2023, les divorces judiciaires
prononcés ont augmenté en 2021, atteignant 65 mille après avoir baissé à 38,8 mille en
2020 (34). Selon l'enquête du lien social de l’IRES de 2024, les formes de sociabilité
imposées par le confinement sanitaire ont contribué au relâchement du lien social et à
l’exacerbation de certains faits sociaux comme le divorce (35). En outre, certaines formes
de divorce subsistent, entraînant des conséquences inéquitables envers les femmes,
telles que le divorce par procuration pour les Marocains résidant à l'étranger, le divorce
moyennant compensation ou le divorce par Khôl.

         En plus de ces constats majeurs, le partage des biens et des propriétés acquis
entre les couples mariés s’avère inadapté, tenant compte de la contribution
substantielle des femmes dans le couple, renforçant le principe de l'équité économique
au sein des unions. La pratique a démontré la non formalisation des contrats de mariage,
l’article 49 ne stipulant pas de dispositions relatives à la manière de fructifier et de
répartir les biens acquis pendant la relation conjugale. Il ne prévoit pas non plus la
possibilité de verser une prestation compensatoire, en y inscrivant la part des acquêts
post-mariage pour reconnaître le travail des femmes pendant la durée du mariage (El
ked wa saaya), leur contribution directe à l'enrichissement des biens familiaux est
difficile à prouver.



                                            22
        En outre, les dispositions sur les droits des enfants, en conformité avec les
instruments internationaux ratifiés par le Maroc, ne répondent pas de manière optimale
au principe fondamental du meilleur intérêt de l'enfant, tel que reconnu par le droit
international. La société fait face également à la persistance du mariage des mineures
reconnu comme une pratique socioculturelle néfaste, aux ambiguïtés dans le processus
de reconnaissance de la paternité et de la filiation paternelle des enfants nés hors
mariage (fiançailles, choubha), qui sont pris en charge par le père et qui octroient le droit
à l'héritage, sous réserve de la preuve de la paternité par des tests ADN.

        Par ailleurs, l'absence de clarté dans la jurisprudence marocaine concernant les
modalités d'établissement de la filiation paternelle, issue des fiançailles, accroît
l'incertitude juridique et la vulnérabilité de la fiancée (36). Selon l'enquête du lien social
de l’IRES de 2024, 73% des enquêtés estiment que le Code de la famille doit être révisé.

       Parmi eux, 21 % souhaitent une révision tenant compte des principes de la
Constitution de 2011, 31 % veulent revoir le fonctionnement des tribunaux de la
famille, et 48 % demandent l'intégration de nouveaux droits en faveur des femmes. Plus
précisément, 32 % des répondants préconisent le partage des biens acquis pendant le
mariage, 20 % l'équité dans les procédures de divorce, 13 % la tutelle des enfants en
cas de divorce, 12 % la fixation du montant de la pension alimentaire lors d'une
séparation, 11 % le mariage des mineurs, et 12 % le statut des enfants nés hors mariage
(37).


        Parallèlement, les chantiers de la réforme du Code Pénal en 2003 et de la
procédure pénale ont été amorcés avec l'incrimination du harcèlement sexuel, grâce à
une révision majeure des sanctions dans les cas de viol, et l'abrogation de dispositions
légales controversées, telles que l'alinéa 2 de l'article 475, qui autorisait le mariage entre
le violeur et sa victime pour échapper aux poursuites.

        Toutefois, la pratique pénale a mis en évidence des défis inhérents au Code
Pénal, révélant un ensemble de zones grises marquées par des imprécisions (38),
notamment, la qualification des éléments constitutifs des délits d'injure et de
diffamation associés aux différentes formes de haine et de violence, l'intégration de
nouvelles définitions et dispositions relatives à l'incrimination des actes de maltraitance,
d'exploitation et de violence. Ces dispositions entraînent des interprétations parfois
divergentes et engendrent des situations où l'application de la loi devient complexe et
suscite des débats juridiques intenses (39). Elles se retrouvent en décalage, ne reflétant
pas pleinement l'esprit constitutionnel axé sur la protection des droits fondamentaux
et les conventions ratifiées.




                                             23
4.2.   Refonte de la politique pénale en matière de protection de la femme contre la
       violence et la discrimination

       Au cours des dernières décennies, le Maroc a entrepris d'importantes réformes
juridiques, dans cette vision, la réforme du système judiciaire a été marquée par la
volonté de consolider l’indépendance du pouvoir judiciaire et de renforcer son rôle dans
la protection des droits et des libertés des citoyen.ne.s. La loi organique relative au
Conseil supérieur du pouvoir judiciaire, conformément à la Constitution, ainsi que la
Charte nationale de réforme de la Justice ont marqué des étapes importantes dans ce
processus.

        Dans l’esprit d’optimiser la protection des femmes contre les violences dans la
société marocaine en mutation, le Maroc a déployé des efforts remarquables pour
renforcer le cadre normatif de lutte contre la violence, avec l’adoption de nouvelles lois
criminalisant la violence dans l’espace public et privé à savoir, la traite humaine et le
harcèlement dans la législation du travail ( loi n°103-13 et loi n° 27-14, loi n° 65-99, loi
n° 19-12), l’instauration des peines alternatives (loi n°43-22), l'interdiction des
publicités discriminatoires à l’encontre de la dignité des femmes (loi n°66-16, loi n°83-
13), la levée des discriminations et la garantie d'accès et d'usage des terres collectives
aux femmes soulaliyates (loi n°62-17, loi n°64-17).

       Malgré les efforts consentis, il apparaît que les femmes continuent de faire face
à des contraintes pour accéder à la justice, en raison des disparités territoriales. Elles
méconnaissent souvent le circuit de prise en charge et les acteurs impliqués. En cas de
violence, elles endurent en silence au sein du couple, faute de protection contre le
conjoint, par crainte de représailles ou à cause de la difficulté de présenter des preuves.
De plus, elles éprouvent des difficultés à dénoncer la violence dans les lieux d'études et
de travail, en raison de l'absence de mécanismes de signalement. D’ailleurs, les données
du Ministère Public de 2021 révèlent que 7 923 cas de violences ont été traités, dont
41,84 % liés à la violence physique et 25,42 % à la violence sexuelle, estimant la violence
conjugale à hauteur de 49,92 % des cas (40).

       De plus, selon l'enquête nationale du lien social de l’IRES de 2024, la majorité
des Marocains considère que les causes de la violence contre les femmes sont
culturelles, avec 36 % attribuées à l'environnement familial et culturel, 39 % à
l'éducation et 14 % au niveau d'instruction du conjoint (41).

       Le Maroc s’est également investi dans l’instauration d’une deuxième génération
de textes juridiques destinés à consacrer le principe d’égalité, de parité et de justice
sociale, en particulier en augmentant la représentation des femmes dans les instances
de décision, principalement dans le domaine politique.

       Concernant la fonction publique, il y a lieu de citer l’adoption du projet de loi
n°30-22 relatif au congé de paternité. Qui plus est, la loi cadre n° 9-21 concernant la
protection sociale, adoptée en 2021, marque un jalon structurant dans l’édification d’un
État social. Elle prévoit la généralisation de la couverture sociale, des allocations
familiales et de la retraite, fondées sur le principe de non-discrimination, assurant ainsi
une approche inclusive à travers des dispositifs tels que le Programme d'Aide Sociale
Directe et le Registre Social Unifié.

                                            24
        Les progrès juridiques accomplis témoignent de la robustesse des réformes
législatives. Pourtant, il est encore trop tôt pour évaluer leur efficacité. D’autant plus
que les discriminations intersectionnelles persistent encore. En effet, les différentes
formes de stratification et de discrimination auxquelles font face les femmes sont
toujours présentes, et handicapent fortement l’épanouissement de la femme dans son
environnement.

        Même si le Maroc a connu de nombreuses avancées institutionnelles et
législatives dans la participation politique des femmes à la gouvernance nationale et
locale, les champs économiques et politiques restent toujours plus ouverts aux
hommes. Les barrières socioculturelles semblent résister à l'égalité, au point que le
risque de perte des acquis reste envisageable.

       L’égalité de droit n’est pas encore atteinte en raison des discriminations qui
demeurent inscrites dans certains textes de lois. Selon les recommandations du dernier
rapport de la Convention sur l’Elimination de toute forme de Discrimination à l’égard
des femmes (42), il conviendrait d’harmoniser davantage les textes en conformité avec la
Constitution et les conventions internationales pour consacrer le principe de l’égalité
entre les femmes et les hommes, en particulier, le Code pénal, le Code de la procédure
pénale et le Code de la famille.

Chapitre 3. La femme marocaine dans l’expectative : des enjeux à
            surmonter
       Le diagnostic multivarié et multidimensionnel de la situation de la femme
marocaine a permis de mettre en avant cinq constats synthétiques : un capital humain
féminin non valorisé, des conditions de vie handicapantes, des mutations sociales mal
accompagnées, des horizons féminins encombrés et des voix de femmes inaudibles.
Chacun de ces constats renvoie à une sphère de progrès potentiellement porteuse de
changement positif si elle est investie à bon escient et qui, au contraire, peut constituer
un handicap dans le processus de développement socio-économique, si elle n’est pas
prise en considération à sa juste mesure.

       Ce chapitre se divise en six sections, chacune se penchant sur les différents
aspects de l'avenir de la femme marocaine. La première section examine le capital
humain féminin en tant que potentiel sous-exploité. La deuxième section explore les
mutations sociales entre avancées et défis. La troisième section aborde les conditions
de vie handicapantes. La quatrième section se penche sur les horizons encombrés
proposés à la femme. Enfin, la cinquième section traite de la participation des femmes
dans la gouvernance.

1. Le capital humain féminin, un potentiel sous-exploité

        Grâce aux efforts continus du Royaume pour la généralisation de l’enseignement
et la prise de conscience croissante des familles quant à l’importance de scolariser leurs
enfants, les indicateurs de l’enseignement ont connu une nette amélioration depuis
l’indépendance, notamment, ces deux dernières décennies.



                                            25
● Ainsi, la généralisation de l’enseignement a été atteinte à 100% dans le cycle
  primaire. La même tendance a été observée au cycle secondaire qualifiant, où ce
  taux a atteint environ 76.9% (2022/2023) (43), en raison de la faiblesse de la
  couverture, dans les communes rurales, par les établissements d’enseignement
  secondaire collégial et secondaire. Pour ce qui est de l’enseignement préscolaire, le
  taux de préscolarisation des enfants de la tranche d’âge 4-5 ans a atteint 76.2%
  (2022/2023) (44) et est en pleine croissance en termes de couverture.

● Ces avancées notoires ont été concrétisées à travers la mise en œuvre de la vision
  stratégique pour l’éducation 2015-2030, laquelle encadre les programmes de
  soutien financier aux familles nécessiteuses afin de couvrir les coûts de la scolarité,
  tels que Tayssir, le programme 1 million de cartables, l’Initiative Nationale pour le
  Développement Humain, l’appui aux transports scolaires et aux cantines scolaires,
  les écoles pionnières, les écoles communautaires, ainsi que le développement
  considérable des infrastructures publiques.

● Grâce à l’effort investi pour généraliser l’enseignement, la scolarisation des filles
  s’est normalisée. Pour tous, l’école est devenue un passage obligatoire préparant la
  transition vers l’âge adulte.


               Figure 1 : Perception des chefs de ménages de l’importance
                           de l’école selon le milieu de résidence




      Source : Enquête Nationale sur les Ménages et l'Education, 2019. INE.CSEFRS.




                                           26
● Toutefois, en dépit des efforts déployés ces dernières décennies, l’offre éducative
  fait face à de nombreux défis, tels que l’abandon scolaire qui a atteint 334.664
  enfants en 2021/2022 (dont 129.594 filles) (45), les contraintes territoriales pour la
  généralisation de l’obligation scolaire collégiale et secondaire, les contraintes liées
  aux conditions d’apprentissage et à la qualité d’encadrement, les inégalités sociales
  des apprenants et d’enseignement au niveau régional, la baisse de motivation du
  corps pédagogique et la désillusion face au système éducatif en tant qu’ascenseur
  social.

● Aussi, les stéréotypes concernant l’orientation scolaire des garçons et des filles
  persistent, orientant souvent les filles dans des cursus liés aux sciences humaines,
  sociales, juridiques ou aux soins aux personnes. Cela ne signifie évidemment pas que
  les cursus scientifiques et techniques sont réservés aux garçons (46), les filles étant
  bel et bien présentes dans les écoles d’ingénieur. D’ailleurs les données d’évaluation
  concernant les performances des élèves montrent que les filles sont autant à l’aise
  dans les langues que dans les mathématiques.

     Figure 2 : Scores moyens des élèves en mathématiques et sciences, selon le genre




         Source : Données PNEA 2019, PISA 2018 et PIRLS 2021(47) INE, CSFRS

● La prévalence de l'analphabétisme féminin au Maroc constitue un défi socio-
  éducatif qui persiste malgré les progrès réalisés au fil des années. Des disparités
  significatives existent entre les régions urbaines et rurales. Plus précisément, les
  femmes des zones rurales ont souvent un accès plus limité à l'éducation tout au long
  de la vie, en raison de l'absence d'infrastructures éducatives adéquates ou de
  conditions de vie décentes leur permettant d’y consacrer du temps.
  L’analphabétisme concerne 42,1% de femmes en 2014 (contre 54,7% en 2004) et
  22,2% d’hommes (contre 30,8% en 2004). Entre 2004 et 2014, le taux
  d’analphabétisme chez les femmes a diminué de 12,6%, tandis que celui des
  hommes n’a diminué que de 8,6% seulement (HCP, RGPH 2014).

● Si la fille a plus accès que ses aînées au système éducatif, les externalités positives
  de l’éducation ne sont pas d’actualité. Considéré parmi les plus bas à l’échelle
  mondiale, le taux d’activité des femmes connaît un déclin qui semble prendre une
  tournure structurelle depuis une vingtaine d’années. En 2022, le taux d’activité des
  femmes était de 19,8 % avec une baisse cumulée de près de 41% de 2000 à 2022
  (HCP,2023).


                                           27
   Globalement dans les zones rurales, ce taux est relativement plus élevé que dans les
   zones urbaines du fait, principalement, de l’activité agricole (familiale, vivrière), avec
   des disparités régionales marquées. Aussi, l’écart avec le taux d’activité masculin est
   d’environ 50 points de pourcentage.

● Plus d'un quart des jeunes âgés de 15 à 24 ans (1,5 million de personnes) au niveau
  national sont actuellement hors du marché du travail (48), n'assistent à aucune école
  et ne suivent aucune formation (Not in Education, Employment, or Training (NEET).
  Parmi eux, près de 72,8% sont des femmes, dont 68,2% détiennent un diplôme et
  40,6% sont mariées (une majorité ayant quitté prématurément l’école) (HCP, 2023).
  Selon le rapport de la rapporteuse spéciale sur la violence contre les femmes, le
  mariage forcé, le mariage précoce et le mariage des mineures représentent une
  forme de violation des droits humains engendrée par la privation de scolarisation et
  l’exposition à la violence et la discrimination (49).


                   Figure 3 : Evolution du taux d’activité par genre en %




     Source : Elaboré par les auteurs (à partir des données de l’Enquête emploi, HCP)

        Il est à noter que la pandémie de la Covid 19 a entraîné des conséquences
brutales sur l’activité professionnelle des femmes, accentuant les inégalités
structurelles préexistantes, tant sur le plan professionnel que personnel. Tout d'abord
sur le plan professionnel, la fermeture de nombreux secteurs d'activité manufacturière,
commerciale, de restauration et de services a entraîné une perte d'emplois importante
pour les femmes. Elles ont ainsi été confrontées à des licenciements massifs,
augmentant leur fragilité économique et contribuant à une précarisation accrue au sein
de la population féminine active. Par ailleurs, la transition vers le travail à distance et
l'augmentation de la charge de travail domestique ont été manifestes, notamment, en
raison de la fermeture des écoles et des services de garde d'enfants. Les femmes ont
dû jongler entre leurs obligations professionnelles et familiales, intensifiant ainsi la
pression sur leur bien-être global.



                                            28
        Des études (50) et analyses (51) indiquent que, globalement, cette régression est
due aux disparités territoriales, aux conditions économiques familiales lourdes, au cadre
légal et réglementaire exclusif, ainsi qu’aux stéréotypes persistants dans notre société.
Ces derniers interviennent encore dans les choix d’études des filles (de nombreuses
filières restent encore majoritairement masculines, notamment, en formation
professionnelle), mais le manque d'opportunités économiques correspondant à leur
niveau de qualification ou répondant à leurs attentes en termes de rémunération, de
flexibilité, de mobilité ou de sécurité, prend de plus en plus le dessus sur toutes les
explications de ce repli.

        L’examen des coûts d’opportunité oriente l’engagement de la femme dans une
carrière professionnelle ou son refus. En particulier, lorsque les coûts de transport au
travail, de restauration, de garde d’enfants et d’aide au foyer se cumulent, les revenus
s’amenuisent. En conséquence, ces femmes se découragent et abandonnent leur
recherche d'emploi, compromettant ainsi leur participation au marché du travail.


● Parallèlement à ce phénomène de « décrochage économique des femmes », le
  chômage des femmes demeure constamment et nettement plus élevé que celui des
  hommes, et ce depuis le début des années 2000. En 2022, selon le HCP, le taux de
  chômage était de 17,2% pour les femmes contre 10,31% pour les hommes. Cet écart
  important entre le chômage féminin et masculin, qui perdure depuis des décennies,
  illustre les difficultés persistantes d’insertion professionnelle des femmes actives au
  Maroc. Les niveaux de chômage élevés chez les femmes diplômées (34,8%) sont
  également révélateurs d’un marché du travail qui ne parvient pas à tirer pleinement
  profit du potentiel féminin qualifié disponible.
                  Figure 4 : Evolution du taux de chômage par genre %




     Source : Elaboré par les auteurs (à partir des données de l’Enquête emploi, HCP)




                                           29
    Enjeu 1 : créer les conditions favorables à l'activité des femmes, développer leurs compétences et
    révéler leurs talents

    Le constat soulève l’enjeu d’un environnement plus favorable à l’activité productive des femmes pour
    permettre leur épanouissement intellectuel et contribuer plus efficacement au développement socio-
    économique du pays.

    ▪ Briser les stéréotypes liés aux mondes masculins et féminins
    Il est essentiel d’encourager l’investissement des filles dans les domaines traditionnellement considérés
    comme masculins, dont ceux liés à l’ingénierie ou aux sciences en général. Qu’il s’agisse d’études ou
    d’emploi, l’activité féminine, qu’elle soit intellectuelle ou productive, doit être reconnue à sa juste
    valeur, à l’égal de l’activité masculine. La question de l'adéquation diplôme-emploi est un véritable
    problème pour les deux sexes mais plus encore pour les jeunes femmes. En outre, la question de
    l’évolution des carrières nécessite une attention particulière. Si celle-ci est évidente pour l’homme, elle
    l’est beaucoup moins pour la femme.

▪      Relever les paris de l’engagement et de la création
    Il est nécessaire de renforcer, de manière structurelle, l'accompagnement professionnel des femmes,
    que ce soit en termes de formation adaptée aux secteurs d'avenir, ou de mesures facilitant la garde
    des enfants pour les mères de famille. L'enjeu est de taille pour assurer de manière durable l'insertion
    professionnelle de cette main-d’œuvre féminine. À cet égard, l’investissement dans le capital humain
    exige la préparation d’une jeunesse instruite, responsable, plus qualifiée et dotée de nouvelles
    aptitudes pour s’adapter à la vitesse des évolutions du monde. Mais aussi, la création d’une offre
    éducative nouvelle et culturelle, garantissant un accès équitable à une éducation de qualité (y compris
    dans les zones rurales et enclavées) et répondant aux nouvelles exigences du marché du travail, pour
    préparer les prochaines générations à ˝la formation tout au long de la vie˝.

▪      Optimiser l’usage des nouvelles technologies

    L’accessibilité aux nouvelles technologies, non seulement en termes d’acquisition d’outils mais aussi
    en termes de connectivité, est une opportunité d’accélération de la transition des statuts des femmes.
    Ces outils sont utilisés pour former et éduquer (en éducation juridique, codage, par exemple) et ces
    réseaux constituent des vecteurs de transmission et de renforcement de politiques publiques.

▪      Investir dans la culture égalitaire
    Des efforts supplémentaires devraient être consentis pour supprimer les barrières de genre, investir
    dans le développement de la petite enfance, et adapter des programmes scolaires aux nouveaux défis
    planétaires pour le développement des capacités cognitives. L’intégration de ces initiatives dès le
    préscolaire devra permettre aux enfants d’intégrer les règles sociales de promotion de l'égalité entre
    les sexes dès le plus jeune âge. Cela permettra de préparer non seulement les enfants, garçons et filles,
    à réussir sur le plan académique, mais aussi à devenir des citoyen.ne.s responsables et éclairés, prêts à
    relever les défis du monde contemporain et ce, en inculquant, en tant que priorité, les valeurs
    universelles (l’égalité, la parité, la responsabilité, la lutte contre les discriminations et la citoyenneté),
    l’autonomie de la réflexion (la pensée systémique, l’esprit critique, le design thinking), le travail de
    groupe (la gestion de projet, la flexibilité) ainsi que le raisonnement méthodique et scientifique
    (l’innovation, l’utilisation des nouvelles approches de la révolution numérique), afin d’assurer une
    formation conforme aux standards d’éducation qui favoriserait la réalisation des potentialités.




                                                            30
2. Des mutations sociales : entre avancées et défis

       Les mutations sociales, bien que porteuses de changements positifs, peuvent
aussi devenir des entraves pour les femmes, notamment lorsqu’il y a résistance d’une
partie de la population masculine.

       Le pays a connu une évolution démographique exponentielle avec une
population passant de 6 millions d’habitants au début du siècle dernier à 33.8 millions
en 2014. La population du Maroc passerait, selon la variante moyenne, à 43,6 millions
en 2050(52). Cette poussée démographique exercera une pression accrue sur les
ressources disponibles mais constituerait également une formidable opportunité de
transformation (1) de la structure économique du pays, d’un côté, et (2) du savoir-vivre
ensemble de l’autre.

● La tendance la plus visible des changements démographiques est la nucléarisation
  des structures familiales. La famille de nos jours est nettement différente de ce
  qu’elle était autrefois, tant au niveau de sa composition qu’au niveau de son
  organisation. La taille moyenne des ménages, qui était de 4,8 personnes en 1960
  (4.3 dans l’urbain et 5.1 dans le rural), est de 4.6 personnes en 2014 (4.2 dans l’urbain
  et 5.3 dans le rural). L’estimation du HCP à l’horizon 2050 est de 3.2 personnes (3
  dans l’urbain et 3.7 dans le rural) (53).

● Ce mouvement de réduction de la taille des foyers s’accompagne d’un recul de l’âge
  au premier mariage, sous l’effet de plusieurs facteurs dont le coût de l’installation en
  ménage et probablement aussi, en gestation, le changement de perspective des
  femmes par rapport aux modalités de contractualisation de la mise en union. Cette
  thématique du mariage nécessite des études approfondies pour aller au-delà des
  perceptions traditionnelles rassurantes et aller au plus près de la réalité pour pouvoir
  mettre en place des politiques publiques adéquates. Selon le HCP, les femmes
  instruites et actives sont plus enclines à se marier avec des hommes d'âge similaire.
  Cela s'explique en partie par leurs chances accrues de rencontrer des hommes de
  leur âge à l'université ou dans les écoles supérieures. De plus, leur autonomie
  financière obtenue grâce à des emplois rémunérés réduit l'attrait pour des hommes
  économiquement supérieurs, souvent plus âgés (54).

● Le nombre de mariages au Maroc a atteint 251 847 contrats en 2022, après une
  baisse significative liée au pic de la crise sanitaire en 2020, où seulement 194 000
  mariages avaient été enregistrés (55). Selon le rapport du Conseil supérieur du
  pouvoir judiciaire de 2024, près de 600 000 cas de divorces ont été enregistrés
  entre 2017 et 2022 (56). Selon l'enquête du lien social de l’IRES de 2024, les formes
  de sociabilité imposées par le confinement sanitaire ont contribué au relâchement
  du lien social et à l’exacerbation de certains faits sociaux comme le divorce (57).

● La dépendance des seniors est plus prononcée parmi les femmes, elle constitue en
  2014, 50,1 % des veuves parmi les âgées de 60 ans et plus et 4,9 % des veufs parmi
  les âgées de 60 ans et plus. En outre, le taux des femmes vivant seules selon le milieu
  de résidence en 2022, est de 30,5% pour les (30 à 59 ans), et 65% pour celles âgées
  de plus de 60 ans (58). Qui plus est, dans les années à venir, le Maroc enregistrerait
  un vieillissement accéléré de sa population.

                                            31
   La proportion des personnes âgées de 60 ans et plus doublerait presque, passant de
   12,2% à 23,2% au cours de la période 2022- 2050, exerçant ainsi une pression sur
   la capacité d’absorption des systèmes de santé et de protection sociale (59).

● La diminution de la taille des cellules familiales pose la question de la persistance
  des solidarités familiales qui demeurait jusqu’à peu, l’unique filet social des
  Marocains. L’institutionnalisation des filets sociaux va certes permettre d’organiser
  et de canaliser les aides de lutte contre la pauvreté (Programme d’aide Social Direct,
  Registre Social Unifié, les programmes d’appui sociaux), mais de nouvelles
  problématiques jusqu’alors marginales apparaissent : la prise en charge des
  personnes âgées et la lutte contre l’isolement social et la marginalité des personnes
  vivant seules, entre autres.

● L’évolution démographique interpelle aussi la question du changement des grilles
  de valeurs. Si l'éducation des enfants sur les valeurs de l'amour des parents, la
  solidarité entre les membres de la famille et le sacrifice des parents pour le bien de
  leurs enfants demeurent fortement ancrés dans l'éducation familiale, certains
  indicateurs suggèrent la montée de l’individualisme au sein du groupe. De fait, les
  valeurs de solidarité, de confiance, d'intégrité et de civisme qui sont largement
  portées par la religion musulmane pourraient être secouées, voire mises à mal, à
  cause de l’individualisme rampant. Dès lors, la question de la transmission des
  valeurs qui définissent la « tamaghribite » est posée.

● La mise en avant de la femme et son irruption sur la scène publique ne manquent
  pas d’entraîner des répercussions sur la gestion des espaces et sur les biens
  communs. Auparavant cantonnée dans l’espace privé du domicile et de la famille, la
  femme a progressivement investi l’espace public, espace jusqu’alors considéré
  masculin, que ce soit du fait de ses activités domestiques ou professionnelles.

  Enjeu 2 : Créer les conditions adaptées pour renforcer la cohésion sociale et la confiance de la femme
  dans le changement, afin d’assurer un équilibre sociétal durable.

  La société marocaine connaît des changements rapides et à plusieurs vitesses. Ces mutations ne
  peuvent se faire sans dégâts tant l’hétérogénéité de la société en termes économique, social et culturel
  est forte, surtout si les politiques d’accompagnement et d’atténuation des inégalités ne sont pas, ou
  sont peu ou mal, mises en œuvre. L’essor démographique s’est accompagné de mutations de fond du
  tissu productif, de la société et des territoires portées par le système de gouvernance, le
  positionnement géostratégique du pays et la cellule familiale. En outre, la manière dont est prise en
  charge la famille nouvelle a une incidence sur la situation des femmes dans la société, sur la cohésion
  sociale et sur « l’habiter collectif ». Ces mutations auront une forte incidence sur le Maroc de demain.
  Dans ces conditions, tout laisser aller ne peut que condamner un avenir prospère. Le rôle de l’Etat est
  ici décisif.

  ▪ Rationaliser l’exploitation des ressources
  L’explosion démographique interroge la viabilité de la gestion actuelle des ressources naturelles, l’eau
  par exemple, ainsi que les déchets induits par la vie moderne qui constituent un véritable défi pour ne
  pas condamner l’espace et la nature marocains. Dans un contexte de changement radical et rapide des
  structures socio-économiques de l’Etat, la tentation est grande de laisser faire les forces en présence.
  Or, la vulnérabilité agro-climato-écologique du pays ne cesse de se confirmer jour après jour.




                                                   32
  ▪ Renforcer la cohésion sociale
  La réduction des foyers a provoqué le relâchement des mécanismes de solidarité des familles élargies
  qui, auparavant, existaient du fait de la cohabitation et de la gestion collective des ressources. Ces
  solidarités doivent être prises en charge par l’État qui doit les contextualiser aux exigences actuelles
  pour faire en sorte que personne, notamment les femmes, ne soit abandonné en marge des
  changements. Et ce, d’autant plus que les valeurs morales évoluent en fonction des mutations des
  conditions de vie. Ces changements ont une incidence directe sur la gestion des biens communs et sur
  l’assignation des espaces privés et publics.

  ▪ Renforcer la confiance de la femme dans le changement
  Les changements induits par la nucléarisation de la famille font que la quête de la liberté et de
  l’autonomisation tant recherchées pèse lourd sur les épaules des femmes : le relâchement de la
  solidarité familiale lui est souvent reproché. L’évolution de la femme marocaine provoque beaucoup
  de remous et souvent de violence tant la présence dans certaines sphères est considérée comme une
  possession de pouvoir. Des règles doivent être posées et des outils créés pour permettre à la femme
  d’occuper le rôle qui devrait être le sien dans une société épanouie.


3. Des conditions de vie handicapantes

La nucléarisation de la famille, conjuguée à l’éducation des filles et à la normalisation
du travail rémunéré féminin, n’a eu que peu de conséquences sur le partage sexué de
la charge de travail domestique qui place encore les rapports femme-homme dans un
schéma classique : les femmes consacrent 7 fois plus de temps que les hommes aux
activités domestiques (60). Cette inégalité est transmise aux jeunes générations
puisque les filles réservent 3,4 fois plus du temps au travail domestique que les garçons,
et que les garçons réservent 1,5 fois plus du temps aux études que les filles.

              Figure 5 : Durée moyenne des activités selon le nombre d’enfants
                                 dans le ménage et le sexe




                        Source : Enquête Nationale sur l’Emploi du Temps, HCP, 2012.




                                                    33
● La transformation de la famille a bouleversé les rôles de ses membres, renforçant la
  charge de travail de la femme à l’intérieur du foyer, du fait de la charge de travail
  domestique et de sa pénibilité concentrée sur ses seules épaules. Or, les ménages
  se trouvent à la croisée des chemins : lorsque la femme n’a pas d’activité rémunérée,
  le niveau de revenu du ménage freine aussi bien sa consommation que ses
  ambitions. Lorsqu’elle travaille, elle supporte une charge mentale conséquente au
  sein des ménages, ne réussissant pas à concilier vie privée et vie professionnelle.

● Le paradigme invisibilisant et démonétisant le travail des femmes est remis en cause
  par les conditions de vie moderne. L’estimation de la valeur du travail domestique,
  en prenant en compte le périmètre restreint des activités humaines (tout ce qui est
  délégable, productif et dont le substitut marchand existe), faite par le HCP,
  augmenterait de 34,5% le PIB (avec une valeur SMIG = 12,24 Dh/h). La charge de
  travail non rémunéré influence directement l'engagement des femmes dans un
  emploi rémunéré. Ainsi, parmi les femmes en âge d'activité, le taux d'emploi est 2
  fois plus élevé chez celles consacrant moins de 2h par jour aux activités domestiques
  que chez celles y consacrant plus de 4h (HCP, 2023).

● Les données de l'enquête sur la violence à l'égard des femmes de 2019 du HCP
  révèlent des réalités préoccupantes au Maroc. Avec plus de 8 femmes sur 10 ayant
  subi au moins un acte de violence au cours de leur vie, ces chiffres soulignent
  l'ampleur du problème. Les tranches d'âge les plus vulnérables sont les jeunes de 15
  à 24 ans. Cela met en lumière l’importance de mener des actions d'intervention
  précoce auprès des plus jeunes. De plus, la violence ne discrimine pas en fonction
  du niveau d'éducation.

   Au contraire, les femmes scolarisées ayant un niveau supérieur semblent être plus
   exposées à la violence à hauteur de 62,7%, suscitant des questions cruciales sur les
   facteurs qui y contribuent tels que l'indépendance financière ou la non-acceptation
   de la réussite professionnelle. D’ailleurs, le contexte conjugal se distingue comme le
   foyer principal de la violence avec un taux de 46,1%, soulignant la nécessité
   d'explorer les nouvelles dynamiques relationnelles des couples et les pressions
   socioculturelles qui peuvent conduire à des comportements violents de la part du
   conjoint. En scrutant les différentes formes de violence, la dimension psychologique
   se démarque à hauteur de 47,5%, mettant en évidence la violence psychologique
   subie, à travers notamment, les comportements intimidants et dévalorisants ou les
   menaces humiliantes.

● Le coût de la vie entraîne des conséquences sous-estimées sur la situation de la
  femme. Plus que les impacts directs sur les ménages, la cherté de la vie constitue un
  véritable obstacle à gérer, souvent au détriment de la femme avant tout autre
  individu dans la famille. Selon la théorie économique du choix rationnel, lorsque les
  ressources se font rares, les consommateurs tendent à minimiser les coûts et à
  maximiser les avantages au travers de leur choix de consommation. Ainsi, dans les
  contextes de difficulté financière, la femme est la première à se priver pour
  permettre aux autres membres de la famille de moins souffrir du manque.




                                           34
● En 2014, au niveau national, le taux de pauvreté multidimensionnelle chez les
  femmes de 18 ans et plus était de 18,1 % (2,05 millions de femmes pauvres). Par
  milieu de résidence, ce taux était de 37,9 % en zone rurale (1,58 million de femmes)
  et de 6,5 % en zone urbaine (470 000 femmes). Ainsi, en 2014, 77,2 % des femmes
  multidimensionnellement pauvres au Maroc vivaient dans les zones rurales (61).

  Enjeu 3 : Favoriser l’épanouissement de la femme

  Cet enjeu aborde les domaines qui freinent l'épanouissement de la fille et de la femme. Pour remédier
  aux insuffisances, il est crucial d’apporter plus d’égalité dans la gestion du foyer familial, et de lutter
  contre la violence basée sur le genre. Ces initiatives permettraient de favoriser l’épanouissement des
  femmes dans l’avenir, de renforcer leur autonomie et de contribuer à une société plus épanouie.

  ▪ Renforcer la famille

  Un partage équitable des tâches et des responsabilités entre parents est bénéfique pour toute la
  famille. Cela permet à chaque parent d'apprécier son rôle, de passer du temps avec son enfant en plus
  de lui permettre de développer une relation significative avec chacun de ses parents. En particulier, il
  est nécessaire que le père joue un rôle actif dans le foyer : les nouveaux pères sont indispensables dans
  les familles de demain pour l’équilibre de la société. Aussi, et surtout, la parentalité positive, aussi bien
  que la participation de l’homme aux tâches ménagères, au soin et l’entretien du foyer, diminue de
  manière consistante la charge mentale portée par la femme, laquelle peut s’investir mieux dans des
  activités professionnelles, au bénéfice de tous.

  ▪ Ne plus composer avec la violence

  Le contexte de changements multidimensionnels provoque de fortes tensions au niveau social qui se
  répercutent sur la femme, étant mal considérée par les lois pénales sur le sujet. Or, ces violences
  entraînent des répercussions indéniables, non seulement sur les victimes mais aussi sur la société dans
  son ensemble, notamment, parce que ces violences se transmettent inter-générationnellement. Le
  manque de confiance qui en découle pénalise très fortement la cohésion sociale et le plein engagement
  des individus dans le développement du pays. Aussi, il est important que la pénalisation des violences
  soit renforcée de manière sévère pour dissuader les personnes à y avoir recours.

  ▪ Permettre aux femmes d’aspirer à une vie meilleure

  Le développement de filets sociaux est essentiel pour soulager les femmes du poids de la survie. Que
  ce soit pour se soigner ou pour pouvoir manger, les personnes les plus défavorisées doivent compter
  sur l’État pour ne pas rester en marge, et les personnes précaires, pour rebondir avec moins de
  difficultés. Le renforcement de l’Etat social est essentiel pour éviter une polarisation insupportable de
  la société.


4. Des horizons encombrés

       Le sous-emploi des femmes est largement influencé par l’inadéquation
formation/emploi ainsi que par la qualité de l’emploi. La prévalence du chômage fait
que les femmes se trouvent souvent dans l’obligation d’accepter des emplois précaires
et générateurs de faibles revenus. Pour pouvoir subvenir à leurs besoins et à ceux de
leurs familles, elles se rabattent sur le sous-emploi. Ainsi, le taux de sous-emploi des
femmes actives occupées a été estimé à 5.4% en 2022(62). Toutes les catégories sont
concernées : 42.4% de femmes sont sans diplôme, 23/1% ont un diplôme moyen et
34.4% ont un diplôme supérieur.


                                                     35
                 Figure 6 : Evolution du taux du sous-emploi par genre %




      Source : Elaboré par les auteurs (à partir des données de l'enquête annuelle sur le
                                   marché du travail HCP).

● Selon le HCP (2020), la part de l'emploi informel dans l'emploi non agricole féminin
  est passée de 53,8% à 67,2% entre 2000 et 2019. Ces emplois informels se
  caractérisent par l'absence de protection sociale et des revenus irréguliers, ce qui
  pointe le manque de contrôle du respect du Code du travail.

● La fonction publique et les services restent les premiers pourvoyeurs d'emplois
  salariés féminins. Le taux de féminisation de l’emploi se situe à des niveaux très
  faibles : 20,8 % pour les salariés, 11,9 % pour les indépendants, 8,7% pour les
  employeurs, 14,5 % pour les apprentis et 9,7 % pour les membres des coopératives.
  Les aides familiales représentent le taux le plus élevé, soit 55,5 %(63).

● La sécurisation de l’emploi a pour prix à payer le bas niveau des rémunérations. En
  2018, la rémunération brute horaire moyenne des femmes salariées était de 15,5
  DH, contre 21,7 DH pour les hommes (HCP, 2021). Dans le secteur public, où les
  hommes perçoivent en moyenne 8 500 DH et les femmes 8 300 DH, l'écart salarial
  se limite à 2,4%. En revanche, dans le secteur privé, les moyennes s'élèvent
  respectivement à 5 400 DH pour les hommes et 3 800 DH pour les femmes,
  entraînant un écart de 43% (64). Ces inégalités entravent significativement les
  perspectives des femmes dans la sphère économique.

● En 2020, 86 % de femmes ont perçu un salaire inférieur au SMAG dans le secteur
  agricole, tandis que le pourcentage attribué aux hommes est de 65 %. Certains
  emplois précaires et informels, notamment agricoles, payent même en-dessous du
  salaire minimum légal. Les inégalités salariales restent une préoccupation,
  notamment dans le secteur privé informel. Bien qu’interdite par le Code de travail,
  cette inégalité prospère en l'absence de mécanismes contraignants de contrôle et
  de sanctions financières dissuasives.




                                            36
                 Figure 7 : L’entreprenariat, poids par genre (18 ans et plus en %)




       Source : Enquête nationale sur le profil entrepreneurial du Maroc (BAD, MEF, 2023)

●   Malgré plusieurs mesures et programmes mis en place, au cours de la dernière
    décennie, pour stimuler l’économie sociale et solidaire et favoriser la formalisation des
    unités économiques informelles, l’entrepreneuriat informel (80%) et celui de
    subsistance (47%) sont plus marqués chez la population féminine (EINA-BAD, MEF,
    2023). Les femmes s’impliquent dans des activités à faible productivité, souvent au sein
    du foyer, et sont donc plus susceptibles d’exercer dans l’informalité. Cette tendance
    pourrait s’expliquer, en partie, par un certain nombre de contraintes institutionnelles
    qui entravent le processus de formalisation et la croissance des entreprises.
    Globalement, l’accès au financement est considéré comme l’obstacle majeur à
    l’entrepreneuriat féminin. Les entrepreneures femmes ont financé leurs activités pour
    plus de la moitié (55%) grâce à l’appui familial. À cela s’ajoute, un manque significatif en
    termes de services d’accompagnement adaptés aux spécificités des femmes
    entrepreneures (EINA-BAD, MEF, 2023). Néanmoins, le secteur du micro-crédit au
    Maroc constitue un potentiel considérable pour la formalisation des activités
    entrepreneuriales féminines en fournissant un appui financier, mais aussi technique.

●   En matière d’émigration, selon les données récentes du HCP (2021), le taux de
    féminisation des migrants est de 31,7%. Majoritairement masculine jusqu'au milieu des
    années 1970, l’émigration féminine a évolué au fil des décennies, d'abord avec le
    regroupement familial, puis avec une émigration de plus en plus autonome soit pour les
    études, soit pour le travail, notamment dans l’agriculture et dans les services. Même si
    le phénomène est encore étudié timidement, les femmes dans la migration
    internationale contribuent dans leur pays au développement économique, matériel,
    culturel et symbolique de leur secteur d’activité, quartier ou village d'origine, surtout
    dans les milieux populaires et ruraux, où le poids de la modernisation se fait moins
    sentir. Les femmes émigrées constituent un agent principal du changement social
    qu’elles soient mères, épouses ou filles, d’autant plus que la démocratisation des
    moyens de communication leur permet de devenir de véritables vecteurs de
    changement, que ce soit en termes d’accès à la citoyenneté, par la participation aux
    débats sociaux et politiques, à travers le partage de bonnes pratiques ou plus
    simplement le maintien du lien social.




                                                37
       Enjeu 4 : Elargir les horizons en facilitant l'accès aux ressources essentielles
       La femme marocaine dispose de plus de possibilités qu’elle n’en a jamais eues dans son histoire pour
       améliorer ses conditions de vie et partant, celles de son entourage. Pourtant, elle est confrontée à
       beaucoup de blocages qui freinent sa transition d’un monde essentiellement intérieur vers le monde
       extérieur.
       ▪ Formaliser l’activité économique
       La femme marocaine travaille et produit mais la plupart du temps de manière invisible ou sous-
       valorisée. Des mesures et des mécanismes de suivi pointus de proximité doivent être créés pour aider
       à la formalisation des activités, ciblant notamment les petites et moyennes entités employant
       majoritairement des femmes. Cela contribuerait à la sécurisation de l’emploi et à la valorisation du
       travail décent.

       ▪ Favoriser l’entrée et sécuriser le maintien en emploi

       Le Code du travail, au-delà du renforcement des mécanismes de sa mise en vigueur effective,
       gagnerait à intégrer des mesures de conciliation vie familiale-vie professionnelle, aussi bien pour
       l’homme que pour la femme. Et ce, afin de permettre aux pères et aux mères d’exercer leurs
       obligations envers leurs ascendants et descendants sans que cela n’influe négativement sur leurs
       carrières professionnelles respectives (mécanismes de gardes d’enfants, congés parentaux partagés,
       emplois du temps aménagés, etc.).

       ▪ Faciliter l'accès aux ressources vitales
       Contribuer à un avenir épanouissant pour les femmes tout en libérant pleinement leurs potentiels,
       nécessite un accès équitable à des ressources cruciales, ce qui a un impact significatif sur l'économie.
       Cela se concrétise par un accompagnement technique et financier adapté pour le perfectionnement
       de leurs compétences professionnelles ou entrepreneuriales. De surcroît, l'accès aux technologies
       numériques, permettant de surmonter les barrières géographiques et d'élargir les opportunités, joue
       un rôle clé dans cette perspective.


    5. Accès fragilisé aux soins de santé
            En 2021, le taux de couverture médicale de base au Maroc a augmenté pour
    atteindre 70% (65), une hausse significative par rapport aux 16% enregistrés en 2005.
    Cette progression est due à l'inclusion des professions libérales et des travailleurs non-
    salariés, et le basculement des Ramedistes. Cependant, selon l’étude de l’ONDH sur les
    discriminations intersectionnelles de 2020, près de la moitié des femmes marocaines
    ne dispose d’aucune couverture médicale : 44,6% ne sont ni adhérentes ni bénéficiaires
    d’aucun des systèmes d’assurance-maladie (AMO) (66). Ce taux moyen cache de fortes
    inégalités entre les femmes. En milieu urbain, le taux de privation par rapport à
    l’assurance-maladie atteint 39,2%. IL est de l’ordre de 53,7% en milieu rural. Selon les
    quintiles de dépenses, les femmes les plus riches ont un taux de privation de 33,2% et
    les femmes les plus pauvres ont un taux qui atteint 51,8% (67).

●   La prévalence déclarée de maladies chroniques chez les femmes, selon l’étude du
    MSPS, à titre d’exemple, l’hypertension artérielle de la population âgée de 18 ans,
    concerne 13,4% de femmes et 6.9% d’hommes déclarés. En outre, la prévalence du
    diabète est déclarée chez les femmes à 8.2%, elle est supérieure à celle des hommes
    (5.9%). La prévalence déclarée des maladies chroniques de la population âgée de 18
    ans et plus est de 34.5% des femmes. Celles-ci sont nettement plus touchées que les
    hommes (23.1%) (68). Depuis 2023, plus de 50 000 cas de cancers sont dépistés
    annuellement (69). Cette maladie commence à constituer un problème de santé publique
    majeur.

                                                         38
●   En 2022, l'espérance de vie est plus élevée pour les femmes à hauteur de 78,6 ans en
    2022, celle des hommes est de 75,2 ans en 2022 (70). Ce gain est une résultante de la
    baisse de la mortalité aux différents âges et de l’amélioration des conditions de vie et
    de santé.

●   L’indice synthétique de fécondité poursuit sa baisse entamée depuis le milieu des
    années 1980. Ainsi, de 1994 à 2014, il est passé de 3,28 à 2,21 enfants par femme et
    il frôle le seuil de remplacement des générations en 2022, atteignant 2,1 enfants par
    femme (71).

●   La réduction des mortalités maternelles de 78% sur 25 ans, est passée de 332 décès
    en 1992 à 72,6 décès pour 100.000 naissances vivantes en 2016.Aussi, elle Est de 72
    décès pour 100 000 naissances vivantes en 2020, soit une régression de 36%(72).
    Cependant, le fossé entre les deux milieux, urbain et rural, est resté pratiquement le
    même durant les 30 dernières années (73).

●   Le pourcentage de morbidité déclarée affecte les femmes (14.7%) plus que les hommes
    (11.3%) et les citadins (13.9%) plus que les ruraux (11.6%) (74).

●   Les mineures mariées ont un accès limité aux services de santé. En 2018, le taux de
    fécondité parmi les adolescentes âgées de 15 à 19 ans s'élève à 19,4‰ (75). Ce taux
    atteignait encore 22,5‰ en milieu rural, soit le double de celui en milieu urbain
    (11,5‰). Selon le Ministère de la Justice, le nombre total de demandes de mariage qui
    a été accordées entre 2009 et 2018 s’élève à environ 319.177 cas (76).

●   Le pourcentage d’obésité est plus exacerbé chez les femmes qui sont presque 3 fois
    plus exposées à l’obésité (29%) que les hommes (11%). L’iniquité sévère est confirmée
    par l’indice de dissimilarité qui atteint 17.9%(77).

●   L'âge du mariage est de plus en plus tardif. En 1960, les femmes entraient en union à
    l’âge de 17,5 ans en moyenne (43 années d’espérance de vie) et les hommes à 24 ans
    (41 années d’espérance de vie (78). Actuellement, l’âge moyen au premier mariage des
    femmes dépasse 25 ans et 30 ans chez les hommes.

●   La santé mentale, le taux de mortalité par suicide était de 7,2 pour 100 000 habitants,
    avec un taux de 4,7 pour les femmes et de 9,7 pour les hommes, selon les estimations
    de l’OMS. En 2020, les autorités ont intervenu pour 1 719 tentatives de suicide (79).

●   La contraception a mis beaucoup de temps à s’imposer au sein des ménages (80), et
    beaucoup reste à faire. En effet, selon l’ENPSF-2018, le taux d’utilisation d’une
    méthode contraceptive quelle qu’elle soit chez les femmes non célibataires âgées de
    15 à 49 ans est de 70,8% (contre 67,4% en 2014) (81). Ce qui indique que presque 30%
    des femmes non célibataires n’ont accès à l’utilisation d’aucune méthode contraceptive.
    Pour ce qui est de la contraception masculine, elle est encore taboue.

●   L’interruption volontaire de grossesse est toujours un sujet difficile à aborder.
    Considérée comme marqueur de l’émancipation sexuelle de la femme, sa prise en
    charge institutionnelle reste très restreinte, malgré ses nombreux impacts sur la santé
    des femmes pour ce qui est des avortements non encadrés médicalement. Cela reste
    un phénomène difficilement abordable statistiquement.

                                              39
   Enjeu 5 : Investir dans le bien-être et la santé de la femme
   Cet enjeu aborde les questions liées à l’accès égalitaire à la santé et son lien avec le bien-être des
   femmes. Pour remédier aux insuffisances, il est crucial de garantir un accès équitable aux services de
   santé sexuelle et reproductive et de mettre en œuvre des mesures pour protéger la santé de la femme
   en général, et de la mère en particulier Ces initiatives permettraient de favoriser le bien-être global des
   femmes dans l’avenir, et de renforcer leur autonomie.
   ▪ Sécuriser l’acte de mettre au monde
   L’enfantement n’est pas une chose banale. Il implique une responsabilité qu’aussi bien l’homme que la
   femme doit assumer. Dans ce sens, la contraception, aussi bien féminine que masculine, doit se
   généraliser et être à portée de toutes et tous pour permettre à chacun de mieux contrôler sa vie. En
   plus, l’encadrement juridique de l’avortement doit prendre en considération les mutations sociales,
   pour éviter les drames vécus quotidiennement par un grand nombre de femmes.

   ▪ Favoriser l’accès aux soins à la population et développer une offre médicale de qualité
   L’augmentation de l'espérance de vie et le développement de maladies chroniques imposent une
   attention particulière au secteur de la santé. La question des inégalités d’accès et de la qualité de l’offre
   médicale va représenter un enjeu d’avenir déterminant pour l’ensemble de la population. Une
   population en mauvaise santé affecte aussi la compétitivité du pays, que ce soit directement du fait de
   ressources humaines affaiblies, ou indirectement avec des inégalités sociales criantes impactant
   négativement le climat social. Également, la prise en considération des maladies dites modernes va
   nécessiter, non seulement une révolution de l’offre médicale, mais aussi des prises en charge.


  6. Des voix féminines inaudibles

          La promotion de la participation politique des femmes est cruciale pour la
  réalisation des Objectifs de Développement Durable (82). La proportion minimale,
  généralement considérée suffisante pour assurer une masse critique de femmes au
  Parlement, a été fixée à 30 % par la plateforme de Beijing. Ce seuil constitue un
  indicateur d’analyse de l’évolution de la participation politique et institutionnelle des
  femmes.

● La Constitution prévoit la parité dans la participation politique dans les articles 30 (83),
  et 146 (84). Plusieurs mécanismes, législatifs et institutionnels, de promotion de la
  participation des femmes à la sphère de décision politique et publique ont été adoptés
  pour concrétiser les principes d’égalité et de parité stipulés dans ces articles : quota,
  liste réservée, siège annexe, etc. Pourtant, douze ans après l’adoption de la
  Constitution, si la représentation politique des femmes est en progression depuis le
  début des années 2000 en raison de mécanismes de discrimination positive, elle est
  toutefois trop lente. Aussi, la masse critique de 30% n’étant pas encore atteinte, les
  élues trouvent des difficultés pour exercer une réelle influence sur les décisions, les
  champs décisionnels demeurant résolument masculins.
● L’entrée des femmes sur la scène de la gouvernance locale, relativement limitée de
  1960 à 2003, a évolué positivement depuis 2009. Si, en 2003, le taux de féminisation
  des Conseils élus locaux était faible (0,54%), la participation des femmes aux élections
  communales a pu passer la barre des 10% en 2009 et a progressivement évolué au
  cours des échéances électorales pour se situer à 21.18% en 2015 (tableau n°1).




                                                       40
Par ailleurs, selon les données du HCP en 2023, la part des postes élus occupés par les
femmes dans les organes délibérants des Conseils communaux a évolué de 12.33% en
2009 à 26.64% en 2021, et dans les Conseils régionaux de 2.21% à 38.50%. Les acquis
restent néanmoins très mitigés car l’accès à la gestion politique, au sein des organes de
décision des collectivités territoriales, demeure encore fortement masculin, les femmes
étant relativement peu présentes au sein des instances exécutives (85).


            Tableau 1 : Représentation des femmes aux élections communales

                     Candidates                             Élues
                                            Total
                                                                            Total Élues
                                          candidats
                    Nb            %                    Nb           %


         1960             14                  17.174         0

         1976             76       0.18       42.638         0       0.07        13.358

         1983            307       0.56       54.469        43       0.28        15.493

         1992         1.086        1.16       93.773         77      0.35        22.240

         1997         1.651        1.61      122.658         83      0.34        24.236

         2003         6.024        4.91      122.658        127      0.54        23.689

        2009*        20.327       15.60      130.305    3.424       12.33        27.665

        2015*        28.725       21.94      130.305    6.669       21.18        31.482

        2021*        47.087       29.87      157.642    8.863       26.64        32.513

   Source : Evaluation des mécanismes de promotion de la représentation politique des
      femmes au Maroc, Jossour Forum des femmes marocaines, Novembre 2017/
                            *Actualisation Chiffres HCP 2023

        Si la représentation des femmes au sein du parlement a évolué entre 2002 et
 2021, elle demeure limitée et sans réel accès aux postes de responsabilité. En 2002,
 la liste nationale a en effet permis l’entrée de 30 femmes à la Chambre des
 représentants, dont 5 par le biais des listes locales, soit 11% du total des membres de
 la Chambre des représentants. En 2011, elle a permis l’entrée de 60 femmes issues de
 la liste nationale des femmes et 7 par le biais des circonscriptions locales (16,96%), et
 en 2016, 81 femmes ont rejoint la première chambre (20,51%). En 2021, ce nombre
 est passé à 96 femmes (24,3%) (voir tableau n°1).




                                              41
            Tableau 2 : Représentation des femmes aux élections législatives

                      Candidates                            Élues
                                            Total
                                                                            Total Élues
                                          candidats
                    Nb        %                        Nb           %


          1963        16           2.32         690         0                         144

          1977           8         1.13         706         0                         176

          1984        15           1.13        1.333        0                         199

          1993        33           1.64        2.009        2        0.90             222

          1997        69           2.10        3.288        2        0.62     325 + 2 CC

          2002       266           4.54        5.865        35      10.77     325 + 2 CC

          2007       269           4.02        6.691        34      10.46     325 + 2 CC

          2011      1.624     22.87            7.102        67      16.96     395 + 6 CC

          2016*     2.081     30.66            6.897        81      20.51    395 + 14 CC

          2021*     2.334     34.20            6.824        96      24.30    395 + 15 CC

     Source : Evaluation des mécanismes de promotion de la représentation politique des
           femmes au Maroc, Jossour Forum des femmes marocaines, Novembre
                           2017/*Actualisation Chiffres HCP 2023


       Au niveau de la Chambre des Conseillers, le nombre de femmes siégeant au sein
de cette institution a évolué. Il est passé de 6 membres en 2011 (2, 2%) à 14 en 2016
(11,7) et à 15 en 2021 (12,5), (voir tableau n°2), la procédure d’élection étant un
cheminement complexe et discriminatoire pour les femmes. A ce sujet, selon une étude
de l’OCDE, « l’égal accès des femmes et des hommes dans les postes de décision de
l’administration parlementaire, mais aussi la prise en compte des besoins spécifiques
des femmes dans l’organisation et le fonctionnement du Parlement doivent être
également consolidés afin de permettre aux femmes de pouvoir participer à la vie
parlementaire d’égal à égal avec les hommes » (86).

       La présence des femmes dans le gouvernement a peu évolué. Elle est passée de
12,8 % en 2011, à 16,7% en 2019 et à 24% en 2022 (87). Plusieurs gouvernements se
sont succédés depuis la Constitution de 2011 sans que le taux de représentation puisse
égaler ou dépasser les 30%, requis pour constituer une masse critique apte à peser sur
la décision gouvernementale.




                                                42
       La loi organique n° 29-11 relative aux partis politiques, promulguée le 22
octobre 2011 stipule, dans son article 26, que les partis politiques “œuvrent à
promouvoir et renforcer la participation des femmes et des jeunes dans le
développement politique du pays”. Ils “œuvrent” à cet effet à atteindre la proportion
d’un tiers de participation des femmes dans les organes dirigeants aux niveaux national
et régional, dans le but de la réalisation, à terme, et d’une manière progressive, du
principe de la parité entre les hommes et les femmes” (88).

        Néanmoins, cette mesure n’est pas contraignante, l’article 26 utilisant le verbe
“œuvre” et ne mentionnant aucune sanction dans le cas de son non-respect. Dans la
réalité, les obstacles socioculturels, politiques, économiques et institutionnels limitent
la participation des femmes à la vie politique. Les partis politiques ont souvent du mal
à se défaire de la vision et des pratiques masculines de la politique qui dominent et à
provoquer les changements nécessaires pour renouveler leur fonctionnement et leur
structure, en prenant en compte le principe de l’égalité femme-homme.

       Par ailleurs, les partis politiques, en se limitant de manière presque systématique
à la seule application des quotas ou sièges réservés, prévus par la loi pour les femmes
lors des opérations électorales, se déchargent de leurs responsabilités démocratiques
envers les femmes et les nouvelles générations. Ce faisant, ils instaurent une
compétitivité qui affecte la sororité et la solidarité entre les femmes lors des
candidatures internes et créent des effets négatifs au lieu d’une dynamique positive
d’engagement et d’implication des femmes.

       La loi organique n°02.12 relative aux nominations aux hautes fonctions, adoptée
en application des articles 49 et 92 de la Constitution, ne comprend aucune disposition
spécifique pour concrétiser la parité mentionnée dans son article. Cela se reflète sur
l’accès des femmes aux hautes fonctions au sein de l’administration publique. Ainsi, si
au niveau des fonctions de chef de service et de chef de division, le pourcentage de
femmes est quelque peu élevé bien qu’insuffisant, il tend à décroître au fur et à mesure
que l’on s’élève dans la hiérarchie. A titre d’exemple, entre 2009 et 2022, le nombre de
femmes secrétaires générales est passé de 2 à 4, celui d’inspectrices générales de 2 à
3, de directrices de 40 à 49 et aucune présidente d’université n’a été nommée en 2022.

       De même, le taux de femmes ambassadrices n’a évolué que de 11,5% en 2010 à
20,4% en 2022(89). Selon l’Enquête Gouvernance et Parité « Women on Boards in
Morocco » menée par le Club des femmes administratrices et la Société financière
internationale (SFI) (90), « les organes de gouvernance des entreprises marocaines
souffrent d’un manque de diversité de genre, et rares sont celles où les femmes président
leurs Conseils d’Administration ou de Surveillance ». En effet, plus de 85% des Conseils
sont présidés par un homme. Les Conseils présidés par une femme sont principalement
ceux des entreprises employant moins de 100 personnes avec un actionnariat familial
(56%) et les Conseils des entreprises publiques (25%).

       Par ailleurs, les femmes participent à près de 85% des Comités d’investissement
et 62% des Comités d’audit. La présence des femmes reste très faible dans des Comités
aussi névralgiques et indispensables aux entreprises que les comités stratégiques, et
surtout au niveau des comités des nominations et rémunérations. Le chemin semble
encore long avant une réelle contribution féminine à la décision économique.

                                           43
Enjeu 6 : Renforcer la participation de la femme aux systèmes de gouvernance
Ces quelques données montrent que les systèmes de gouvernance se conjuguent incontestablement
encore au masculin à tous les niveaux, les femmes marocaines continuant de faire l’objet de
discriminations et de déni d’égalité des chances au niveau des postes de décision. Cela pose la
question de l’effectivité des principes constitutionnels face à plusieurs facteurs d’ordre structurel, en
particulier les barrières socioculturelles qui contribuent à perpétuer les stéréotypes et les perceptions
archaïques, ou encore d’ordre législatif en raison d’un arsenal juridique insuffisant qui ne prévoit pas
de mesures coercitives et qui permet de larges interprétations, et ce en l’absence d’un organe
institutionnel pour superviser l’applicabilité des législations, un des rôles qui devrait revenir à
l’Autorité pour la parité et la lutte contre toute forme de discrimination (APALD), prévue par la
Constitution. Cela tend à rendre non opérationnels ou du moins inefficaces les mécanismes et
politiques de promotion de la place des femmes dans les systèmes de gouvernance.

▪ La présence égalitaire et paritaire des femmes dans les systèmes de gouvernance, enjeu du
  développement

Le Maroc ne peut faire l’économie de l’intégration de la moitié de la population aux systèmes de
gouvernance à tous les niveaux et dans les différents domaines, s’il souhaite consolider son lien social,
améliorer ses performances et gagner le défi de devenir une puissance régionale stratégiquement
incontournable.
Les systèmes de discrimination positive ayant montré leurs limites intrinsèques, et compte tenu des
expériences et des pratiques dans le monde, il apparaît plus judicieux de surmonter les difficultés, en
optant pour des solutions aptes à permettre de réussir rapidement et de manière efficace l’implication
globale des femmes. Les femmes ne peuvent plus être éternellement réduites à une affaire de quota.
Provoquer le changement et donner aux femmes l’accès au pouvoir suppose de revoir les techniques
d’inclusion des femmes dans les systèmes de gouvernance pour qu’elles soient plus volontaristes. La
mise en œuvre de la parité inscrite dans la Constitution constitue le meilleur moyen pour y parvenir.
Elle est la condition de l’édification d’un Maroc démocratique, moderne et tourné vers l’avenir.

▪ La consolidation de l’arsenal juridique, enjeu d’un système égalitaire pour les femmes

La mise en œuvre de l’article 19 de la Constitution devient une nécessité urgente. Pour être efficace,
elle suppose une mise à niveau globale de l’ensemble de l’arsenal juridique sous l’angle de la parité et
de l’égalité. Les textes de lois dans les différents domaines institutionnel, socio-économique, culturel
ou environnemental ne contiennent pas de mesures spécifiques relatives à l’introduction de la parité
femme-homme. La consolidation de l’arsenal juridique permettrait de renforcer la présence des
femmes dans les systèmes de gouvernance à tous les niveaux, afin de garantir leur pleine participation
à la prise de décision.

▪ L’effectivité des dispositions juridiques et l’amélioration des pratiques judiciaires, enjeu d’un
  système égalitaire efficace

Si la consolidation de l’arsenal juridique constitue une condition de l’effectivité du droit à la parité, elle
n’en demeure pas moins insuffisante sans la garantie du respect de ses dispositions, d’où l’importance
de mesures aptes à assurer l’effectivité réelle des lois, dont notamment l’introduction de dispositions
de coercition dans les textes de lois et la lutte contre la corruption.




                                                    44
Deuxième partie

Anticiper : Prospective et nœuds du futur à surmonter pour
            l'avenir des femmes
       Cette partie consacrée à la vision prospective s’articule en trois chapitres : aux
nœuds qui entravent l’avancée de la femme marocaine et qui, s’ils étaient pris en
considération, pourraient améliorer sa situation et accélérer de manière significative le
développement du pays, un deuxième autour des scénarios, et un dernier concernant
les axes de dépassement.

Chapitre 4. Identification et analyse des nœuds du futur inhérents à la
             condition de la femme
        Depuis 40 ans, la question de l’amélioration des conditions des femmes est
inscrite au cœur des Orientations Royales et des agendas gouvernementaux. Aussi,
l'analyse des rapports entre les femmes et les hommes, sous l'angle de la construction
sociale, émerge comme un thème d'une importance croissante pour ceux qui se
penchent sur les questions de développement au Maroc.

        En effet, il devient de plus en plus manifeste que, malgré une semblance d'égalité
en matière d’opportunités entre hommes et femmes, la réalité, mise en lumière par les
statistiques officielles, révèle que la société et l'économie marocaine continuent
d'exclure une part significative de la population féminine quant à la possibilité de mener
une existence digne et épanouie. Bien que les femmes puissent théoriquement accéder
aux mêmes droits que les hommes, les disparités persistantes et les barrières
systémiques entravent encore l'effectivité de l’égalité et la parité, et la pleine
participation des femmes dans tous les secteurs de la vie institutionnelle, sociale et
économique.

      C’est dans la perspective de dépasser ces dernières que cette réflexion met en
évidence des scénarios prospectifs de l’avenir de la femme marocaine à l'horizon 2050.
Ces projections tiennent compte des variables clés susceptibles d'affecter l'existence
des femmes et les changements de perspective du contexte socio-économique national
et mondial.

        Ce chapitre consacré aux éléments permanents et aux nœuds leviers du système
étudié s’articule en deux sections. La première section se penche sur les tendances
lourdes qui ont un impact sur la femme marocaine et qui, en toute vraisemblance,
n’évolueront que peu. La deuxième section présente les nœuds qui entravent l’avancée
de la femme marocaine et qui, s’ils étaient abordés, pourraient améliorer sa situation et
accélérer de manière significative le développement du pays.




                                           45
1. Les tendances lourdes

           L’identification des tendances lourdes qui parcourent le système prospectif est
   indispensable à l’élaboration des futurs possibles et la construction des scénarios
   prospectifs. L’évolution de ces tendances se caractérise par une lenteur dans le temps
   car soumises à des variables qui, du fait de leur complexité, s’illustrent par une
   dynamique qui ne peut s’interrompre facilement et dans un temps court, sauf rupture
   brutale. Aussi, la probabilité qu’elles se maintiennent et conditionnent le futur apparaît
   très élevée.

            Le repérage d’une tendance lourde permet donc d’établir des éléments
   prospectifs préconnus et, conséquemment, d’anticiper des avenirs probables à partir de
   l’analyse approfondie des processus dominants. Dans notre cas de figure, trois
   tendances lourdes ont été identifiées : la famille et le lien social comme fondement de
   la société, la culture marocaine comme socle identitaire et un environnement naturel
   fragile.

   1.1.   La famille et le lien social comme fondement de la société

          Dans une société en mutation accélérée, la femme marocaine fait face au bipôle
   modernité-tradition (91). Cependant, alors que le socle de valeurs des Marocaines et
   Marocains semblait être grandement malmené face à la globalisation et la circulation
   des informations, la pandémie de la Covid 19 a permis de révéler ce qui comptait le plus
   pour la population : la famille, en tant qu’entité structurelle de base de la société. Ainsi,
   en 2023, 67% des enquêtés considèrent que le lien familial est fort et 26% qu’il est
   moyen (92).

          Structure de repli lorsque tout va mal, la famille est aussi l’entité de protection
   et de soin pour assurer à ses membres une vie sociale épanouie et ambitieuse. Les
   parents et personnes âgées restent les personnes les plus respectées de la société alors
   que les enfants continuent d’incarner pour leurs parents les espoirs d’une vie meilleure.

           Le lien social est également survalorisé au Maroc. L’importance de privilégier la
   discussion à la confrontation et de maintenir un lien, aussi ténu soit-il, entre toutes les
   composantes de la société donne l’image d’un peuple bienveillant, accueillant et
   solidaire. Cette caractéristique ne manque pas de se révéler à chaque moment de crise,
   la dernière en date étant le tremblement de terre qui a touché la région du Haouz en
   septembre 2023.




                                                46
   1.2.   La culture marocaine, socle de l’identité

           Fort de son histoire civilisationnelle « forgée par la convergence de ses
   composantes arabo-islamique, amazighe et saharo-hassanie, enrichie de ses affluents
   africains, andalou, hébraïque et méditerranéen » (93), le Royaume dispose d’une identité
   fondée sur la richesse de son patrimoine et sa diversité culturelle. La transmission, au
   cours des siècles, de fortes valeurs d’appartenance et de solidarités, se manifestant par
   une créativité dense et exceptionnelle, a permis, tout en s’adaptant aux évolutions et
   mutations sociétales, une dynamique de changement dialectique, lente et progressive,
   qui n’a jamais dévoyé ses racines.

           Si les différents aspects de cette culture ne sont pas encore suffisamment
   valorisés ni même profondément connus, beaucoup restant à dévoiler et comprendre,
   ils n’en sont pas moins présents sur tous les territoires du pays et circulent au gré des
   migrations des populations. La forte conscience collective de cette richesse constitue
   un puissant moteur pour le développement du pays.

   1.3.   Un environnement naturel de plus en plus instable

          Le Maroc, confronté aux conséquences grandissantes des changements
   climatiques voit émerger des menaces sérieuses pour divers secteurs économiques qui
   impactent les femmes, particulièrement l'agriculture, en raison de l'augmentation des
   températures moyennes, de la diminution des précipitations et de la fréquence accrue
   d'événements climatiques extrêmes.

          Ces évolutions impactent déjà sévèrement des bassins de production agricole
   cruciaux (94). Cette fragilité de l’environnement national n’est cependant pas une
   nouveauté : le Maroc a déjà connu des épisodes historiques de modification de ses
   paramètres environnementaux.

          Historiquement, la population s’est toujours adaptée aux changements
   climatiques, en témoigne le riche patrimoine culturel accumulé dans divers domaines,
   tels que l’architecture, l'ingénierie de l’eau ou encore les pratiques de conservation des
   produits de première nécessité. Si les politiques économiques récentes concernant la
   protection du patrimoine naturel sont agressives, il est nécessaire de prendre en
   considération le riche savoir des femmes à ce sujet, et d’envisager les caractéristiques
   naturelles du territoire à leur juste valeur dans la définition même des politiques
   publiques.

2. Nœuds leviers pour tracer un avenir meilleur des femmes

          L’analyse de la condition des femmes au Maroc révèle un certain nombre de
   problématiques dont les impacts peuvent s’avérer importants surtout lorsqu’on tient
   compte des interdépendances entre les dimensions juridiques, sociales, économiques
   et politiques. Les nœuds représentent une concentration d’enjeux complexes qui
   freinent l’évolution positive de la situation de la femme et constituent tout du moins, si
   ce n’est des facteurs de blocage, des facteurs de ralentissement importants, pénalisant
   également le développement socio-économique du pays, ainsi que la réussite des
   politiques publiques mises en place.

                                              47
        Ces nœuds sont nombreux du fait de la présence de la femme dans toutes les
dimensions de la vie sociale, politique et économique du pays. Cependant, l’analyse
structurelle a permis de faire ressortir cinq éléments pouvant servir de nœuds leviers,
qui pourraient agir directement sur les autres nœuds et sur lesquels s’appuyer pour
fluidifier le processus d’évolution positive du Maroc.

2.1.   Le nœud des normes sociales discriminantes qui exacerbent les disparités

       La mobilisation de la culture pour justifier des normes sociales discriminantes
ancrées dans certaines traditions de manière réelle ou chimérique représente une
source de préoccupation majeure en termes de perspectives futures. Ces normes sont
inspirées de croyances, de valeurs ou encore de l'interprétation du religieux, et elles se
manifestent à travers diverses pratiques et attitudes discriminatoires qui limitent l'accès
des femmes à leurs droits fondamentaux et les assignent à des espaces contraints.
        De fait, l'accès des femmes aux ressources et services essentiels est remis en
cause, ce qui peut contribuer à perpétuer les inégalités sociales et économiques, et
entraver le développement inclusif et durable du pays. Les indicateurs internationaux
fournissent une perspective détaillée du retard que le Maroc a accumulé dans la
promotion de la culture de l'égalité des sexes (95), mettant en lumière la complexité
multifacette de cette question, exacerbée par des disparités sociales, de genre et
territoriales.
       Ce nœud s’alimente à partir de quatre constats clairs, constituant eux-mêmes
des nœuds secondaires : une culture égalitaire mitigée, des stéréotypes de genre
ancrés, une interprétation restrictive du religieux dans les droits familiaux et une faible
effectivité des lois et textes réglementaires.
● Une culture égalitaire mitigée
       Malgré la philosophie égalitaire inscrite dans la Constitution de 2011, visant à
réduire les disparités entre les femmes et les hommes dans les domaines sociaux,
économiques, politiques, culturels et environnementaux, tant dans les sphères
publiques que privées, son effectivité et l'acceptation de la culture égalitaire restent
contestées.

         Les résultats de l'enquête IMAGES menée dans la région de Rabat-Salé-Kénitra
en 2016 en sont l'illustration : 56 % des hommes et 87 % des femmes interrogés ont
estimé qu'il était nécessaire de multiplier les efforts pour la promotion de l’égalité entre
les femmes et les hommes (96). Les inégalités sont perçues par les citoyen.ne.s comme
un obstacle majeur au vivre-ensemble selon les enquêtes de 2011 et de 2016 de l’IRES
sur le lien social, ce qui risque de menacer la cohésion du corps social.

       Malgré l'adoption progressive d'une terminologie juridique inspirée de la
philosophie des droits humains et de l’égalité, le Maroc demeure confronté à un défi
d'harmonisation entre les valeurs égalitaristes et les valeurs traditionnelles, en raison de
son double référentiel.




                                            48
        Les comportements quotidiens inspirés et influencés par les contraintes de la
vie, qu’elles soient financières ou tout simplement de contexte, sont en porte-à-faux du
discours tenu. D’ailleurs, l’éducation à l’égalité est encore embryonnaire. Les supports
d’éducation comportent encore des références qui continuent d’assigner les filles et
garçons à des rôles prédestinés, sans oublier que les pratiques parentales continuent
de perpétuer de manière plus ou moins consciente ces dictats.
● Des stéréotypes de genre ancrés
        Malgré les progrès accomplis, la quête d'une véritable égalité est confrontée à la
persistance des résistances sociales et culturelles, des normes discriminatoires, des
pratiques préjudiciables comme le mariage des mineur.e.s et la violence basée sur le
genre, ainsi que des barrières à l'accès équitable aux droits fondamentaux
universellement reconnus. En particulier, l’idée que c’est à l’homme de pourvoir aux
besoins financiers familiaux et à la femme de s’occuper du foyer reste majoritaire. Aussi,
le rôle de soin à l’enfant est exclusivement et de manière imposée attribué à la femme,
invisibilisant totalement la paternité.

       D'autres stéréotypes persistent dans la non-reconnaissance du leadership
féminin, en économie mais aussi en politique, contribuant ainsi à maintenir un plafond
de verre et limitant l'accès des femmes aux postes de décision. Les perceptions
inégalitaires des rôles de genre, considérant les femmes comme trop fragiles et
émotives, ce qui entrave leur progression professionnelle par la crainte de l'échec et la
charge mentale qui leur est souvent attribuée. De plus, la censure masculine, résultant
de la peur de la concurrence et du refus de partager le pouvoir, contribue également à
cette situation.
● Une interprétation restrictive du religieux dans les droits familiaux
       Dans la sphère culturelle musulmane, les droits familiaux sont basés sur le
référent religieux et leur évolution est influencée par l'interprétation des préceptes
coraniques, la Sunna et le rite Malékite. L'évolution de ces droits, en particulier ceux
des femmes, fait l'objet d'une controverse au Maroc, en raison de la nécessité
d'harmoniser, d’une part, les textes juridiques avec la réalité vécue des femmes et
d’autre part, le Code de la famille avec les engagements internationaux en faveur des
droits des femmes tout en respectant les principes religieux revisités. Cette dualité
reflète la complexité entourant la réforme du Code de la famille où se chevauchent les
facteurs religieux, politiques, sociaux et culturels.
● La faible effectivité des lois et des textes réglementaires
       La mise en œuvre effective de la loi et des textes réglementaires au Maroc se
heurte à plusieurs obstacles juridiques et institutionnels, aux problèmes de coordination
et de suivi des politiques publiques, particulièrement lorsqu'elles traitent de questions
sensibles ou impliquent des changements sociaux profonds.




                                           49
       Ainsi, le système juridico-judiciaire fait face à une société en mutation constante
qui peut être confrontée à des défis culturels et traditionnels rendant parfois difficile
l'acceptation et la mise en œuvre de certaines lois, notamment celles touchant aux
droits des femmes.

       De plus, la jurisprudence est parfois affectée par les diverses interprétations et
applications des textes par le système judiciaire, et qui sont souvent influencées par des
facteurs professionnels, culturels et sociaux plutôt que par une stricte adhésion à la
normativité juridique (97). Un exemple concret est celui de l’autorisation accordée par
les juges des affaires familiales pour les mariages de mineur.e.s. En 2024, ces
autorisations ont totalisé 15 000, ce qui représente 5,9 % de toutes les unions
enregistrées (98), sans compter les mariages coutumiers qui ne sont pas
systématiquement inclus dans les statistiques officielles (99).

       Le droit coutumier reste prépondérant dans les décisions individuelles et
collectives concernant le mariage et l'héritage, notamment en ce qui concerne la
propriété foncière (100). En dépit de l’adoption de la loi n° 62-17 concernant les terres
collectives, cette situation met en évidence les défis posés par la coexistence d'un droit
statutaire progressiste et d'un droit coutumier conservateur. Ces différences juridiques
créent des réalités distinctes pour les femmes, en fonction de leur lieu de résidence et
du type de droit qui régit leurs communautés.

Les facteurs explicatifs de la perpétuation des normes sociales discriminantes

       Les facteurs sous-jacents au nœud des normes discriminantes sont enracinés
dans les attitudes, le référentiel religieux et les structures sociales, certes de manière
différente selon la classe sociale et le territoire considérés. L’ambivalence du système
juridique consacre, de ce fait, une dualité qui crée une tension entre les droits des
femmes dans l'espace public et ceux dans l'espace privé, nourrissant les débats sur la
spécificité versus l'universalité et opposant les partisans d’une tradition idéalisée à ceux
de la modernité (101).

       Sur le plan religieux, bien que le Maroc promeut un islam ouvert et tolérant qui
se base sur le rite malékite dont l’interprétation privilégie les finalités de la Loi islamique
révélée (al maqâsid), les sources du droit islamique (al usûl), la coutume locale et la
doctrine légale islamique (fiqh) (102), la référence à la tradition juridique islamique ravive
régulièrement des règles ressurgissant du passé.

       Certes, la tradition juridique islamique est une part importante de l'identité
marocaine, toutefois elle devrait être mobilisée pour créer une impulsion du statut des
femmes vers l'avenir, à partir d’une lecture critique du passé et une réévaluation
constante de l'histoire à la lumière du présent. Ce référentiel religieux doit être vivant,
évolutif, créatif, fondé sur la raison (’aql) et la réflexion (ra’y) de l’ijtihad et des maqasid
(103).




                                              50
         Le Discours Royal du Trône, en 2003, le précise clairement ‘’Les Marocains, en
effet, sont restés attachés aux règles du rite malékite qui se caractérise par une souplesse lui
permettant de prendre en compte les desseins et les finalités des préceptes de l’Islam, et aussi
par son ouverture sur la réalité. Ils se sont employés à l’enrichir par l’effort imaginatif de
l’ijtihad, faisant de la sorte la démonstration que la modération allait de pair avec l’essence
même de la personnalité marocaine qui est en perpétuelle interaction avec les cultures et les
civilisations’’.

       Si la religion et la coutume sont souvent mobilisés pour expliquer les situations,
les rapports de pouvoir au sein des couples, des familles ou autres ne doivent pas être
passés sous silence. Ils constituent en effet de puissants facteurs de perpétuation des
inégalités de genre, hommes et femmes n’utilisant pas les mêmes armes et n’ayant, de
toutes les façons, pas les mêmes vécus, attendus pour les uns, imposés pour les autres.

Les mesures entreprises par les autorités publiques en matière d’égalité

        Conscient de la complexité de ces facteurs, le Maroc a consacré le principe
d'égalité entre les femmes et les hommes dans la Constitution de 2011. Il a initié
diverses réformes législatives touchant des domaines clés tels que le Code de la famille,
le Code du commerce, le Code du travail ou le Code de la nationalité.

      Ces réformes ont été accompagnées de politiques publiques telles que le Plan
Gouvernemental pour l’Égalité (PGE I, PGE II, PGE III) et la stratégie Green Inclusive
Smart Social Regeneration, visant à promouvoir une culture respectueuse des droits
humains et à lutter contre les discriminations.

       Parallèlement, de nouvelles institutions et entités gouvernementales ont été
créées, adoptant des approches novatrices pour contrer les discriminations subies par
les femmes, que ce soit au sein de la famille, dans le système éducatif, dans les
interprétations religieuses, à travers les médias ou la culture populaire.

       Cependant, toutes ces initiatives n’ont que des résultats mitigés à cause de la
faiblesse des ressources allouées aux différentes structures créées, et du déficit en
termes de coordination de l’action publique. Des faiblesses persistent en matière
d’implémentation, de suivi et d’évaluation des politiques publiques ainsi que sur le plan
de la déclinaison territoriale des programmes publics.

       Le Maroc a aussi investi depuis 2017 dans la formation des morchidates et la
féminisation du métier des adoules qui étaient exclusivement masculines. Ainsi, les
morchidates jouent un rôle très important en tant que prédicatrices et conseillères
auprès de groupes sociaux populaires désavantagés, pour ce qui est des questions
proprement théologiques liées à la pratique quotidienne de l’islam et des questions de
société. Elles jouent un rôle crucial pour contrecarrer les confusions entre les normes
sociales qui s'entrecroisent souvent avec les règles religieuses.




                                              51
      Il est à noter, également, la Haute autorité de la communication audiovisuelle
joue un rôle essentiel dans le renforcement de la vigilance sociale sur les contenus
médiatiques, en permettant le droit de saisine pour les contenus jugés discriminatoires.

        Malgré cela, l'absence de politiques publiques régissant la culture médiatique
permet une influence considérable dans la propagation des normes discriminatoires, en
particulier dans les médias numériques et les réseaux sociaux. Bien que des initiatives
telles que les comités de parité de 2M et la SNRT et les récompenses pour les publicités
engagées aient été mises en place par 2M, les réseaux sociaux continuent de véhiculer
des représentations stéréotypées des femmes, contribuant ainsi à perpétuer les
inégalités de genre.

Les impacts de la perpétuation des normes sociales discriminantes

       Les normes discriminatoires entravent le développement social, économique et
politique du Maroc, en limitant le plein potentiel des femmes dans leur engagement
dans la société.

       Dans la sphère familiale, ces normes discriminatoires contribuent à la
perpétuation de la violence conjugale et de certains comportements préjudiciables qui
peuvent aboutir à l’éclatement du couple. Il est d’ailleurs à noter, à ce sujet, que la
violence n’est pas uniquement à considérer dans sa dimension physique (coups et
blessures) mais aussi psychologique (harcèlement, humiliations) et économique (le refus
de subvenir à leurs besoins primaires en cas de dépendance à l’homme).

        Sur le plan institutionnel, ces normes discriminatoires se reflètent souvent dans
les lois, les politiques et les pratiques publiques, créant des obstacles à l'accès équitable
aux droits et aux ressources pour les femmes. Le Code de la famille par exemple
mentionne le partage des responsabilités dans la gestion du foyer conjugal, toutefois,
aucun texte juridique ne reconnaît la charge accrue des responsabilités pour les femmes
au sein du foyer.

       Un impact intéressant à étudier du manque d’appréciation des besoins des
femmes sur le moyen et long terme est leur évitement des situations qui prennent leurs
sources dans les normes discriminantes. Concrètement, cela signifie une baisse de
l’engagement marital, de l’engagement professionnel et de l’engagement social collectif
faute de règles reconnaissant sa véritable place dans la société.

2.2.   Le nœud des rapports déséquilibrés engendrés par la mutation de la famille
       Les modèles familiaux connaissent des changements profonds sous l’effet de
plusieurs facteurs dont on peut citer le retard de l’âge au premier mariage, du fait de la
poursuite des études ou d’un choix assumé, mais aussi la diminution du nombre
d’enfants par foyer. La famille élargie laisse place à la famille nucléaire. Cette mutation
s’accompagne d’un changement du contexte socio-économique d’évolution des
familles, initié par la modernisation des secteurs productifs et des modes de vie, et
provoque tout autant de modification des solidarités intra-familiales.




                                             52
● La transformation de l’institution du mariage
        Bien que le mariage soit encore largement considéré comme une valeur
religieuse et sociale de référence, certaines caractéristiques sont à relever dont le net
recul de l’âge moyen au premier mariage, depuis 1960, l’augmentation continue du
célibat, la diminution du mariage endogame ou encore le recul du divorce malgré le
discours ambiant (31% des premiers mariages se terminaient par un divorce en 1960)
(104) et l’essor des familles recomposées. Selon le rapport du Conseil supérieur du

pouvoir judiciaire de 2024, près de 600 000 cas de divorces ont été enregistrés entre
2017 et 2022. Le taux de divortialité (105) est de 50 affaires de divorce recensées pour
100 demandes d’autorisation de mariage déposées (106).

       Si les mariages étaient auparavant une décision qui relevait du choix des parents
avant tout, aujourd’hui la mise en union est devenue un choix personnel. Ce
changement de paradigme est essentiel : de défense des intérêts familiaux, l’union de
deux personnes est devenue défense d’intérêts communs individuels. Il est aisé de
constater dès lors une désacralisation du mariage, une fluidification des relations de
mariage/mise en couple et une affirmation du couple dans le groupe familial. Dans ces
conditions, et au regard de la situation actuelle de la femme, il est à prévoir de fortes
perturbations à venir dans cette institution liée à la remise en cause de la
prépondérance de l’autorité masculine dans le couple, tout du moins le temps que les
mentalités évoluent. Pourtant, les changements risquent de s’imposer plus vite que
prévu notamment du fait de l’action silencieuse des jeunes générations (milleniums,
génération Z ou encore alpha).

● Les inégalités dans le couple
        Les inégalités au sein du couple sont multiples et toujours invisibilisées tant que
la répartition sociale des tâches de l’homme et de la femme est présentée comme
naturelle et immuable. C’est ainsi que les ressources sont montrées comme étant gérées
de façon optimale par l’homme, considéré principal chef de foyer dès lors qu’il existe.
L’homme est érigé en principal pourvoyeur de revenus, y compris lorsque la femme
apporte elle aussi son lot de revenus au ménage, quels qu’en soient la consistance.
Aussi, le salaire féminin n’est considéré que comme salaire d’appoint, même lorsqu’elle
participe à l’acquisition du domicile conjugal. Selon la même logique, l’emploi féminin
n’est qu’une force de travail supplémentaire et non un acteur à part entière. Cela a
toujours justifié les salaires féminins bas, perçus comme compléments au salaire
principal masculin ou servant seulement à couvrir les besoins personnels de la femme.

        L’autre indicateur important est la gestion de l’espace et de la vie familiale. Si la
tradition assigne la femme aux tâches domestiques et de soin aux membres de la famille,
les conditions de cette assignation n’existent plus. Aussi, lorsque la femme décide de
s’engager dans une activité professionnelle rémunérée, ce travail s’ajoute aux autres
tâches sans que le conjoint considère devoir participer concrètement et physiquement
à l’entretien de la famille. Ce cumul de travaux attribués à la femme constitue de
manière évidente un frein à son engagement dans des activités productrices de
richesse.




                                             53
● La transformation des solidarités
       Les solidarités ont considérablement évolué du fait des changements
multidimensionnels que connaît le pays, passant d’un système de protection sociale
exclusivement familial à un système étatique organisé.

       Les solidarités familiales se sont elles-mêmes considérablement modifiées, se
rétrécissant et changeant de nature dans le temps : les réseaux tribaux ont laissé place
aux réseaux familiaux à taille plus humaine, les solidarités à base clanique territorialisée
ont été remplacées par des réseaux de corps ou d’affinités.

        D’un autre côté, depuis l’indépendance et de manière plus accélérée pendant le
Règne de Sa Majesté le Roi Mohamed VI, l’Etat social s’étoffe et devient plus consistant.
Les systèmes de protection sociale qui ne touchaient au Maroc qu’une minorité de la
population, à savoir les fonctionnaires et les travailleurs du secteur formel
essentiellement, sont en cours de généralisation actuellement pour s’étendre aux
travailleurs indépendants et aux travailleurs non-salariés.

        Dans tous les cas de figure d’évolution de ces solidarités, il est à noter que le
Maroc est un pays de moins en moins jeune, comme en témoignent la baisse du poids
démographique relatif aux moins de 15 ans (44,3 % de la population totale en 1960 et
17,2 % en 2050) et la hausse du poids relatif à la tranche des 60 ans et plus (8,4 % de
la population en 2010, 24,5 % en 2050), selon les projections démographiques du HCP.
Aussi, qu’il s’agisse de solidarités familiales ou institutionnalisées, la protection de la
population va constituer le garant principal de l’édification de l’État de droit moderne.
Si auparavant, les déficiences de l’État étaient compensées par les filets de soutien
familial, ce ne sera bientôt plus possible du fait du rétrécissement des catégories les
plus jeunes. La solidarité intergénérationnelle est indispensable pour l’édification de
l'État social.

● La faiblesse des infrastructures sociales publiques
       Si la perception du rôle de la femme dans la société est si mal appréhendée et
mesurée, c’est parce que ce sujet est confiné dans la sphère privée et considéré comme
étant de l’ordre de l’évidence, conformément aux traditions et aux coutumes, donc
comme étant un non-sujet.

        L’existence d’infrastructures sociales devrait permettre de dévoiler les
innombrables écueils que la femme doit éviter le long de son existence et pourrait
contribuer à faire évoluer les comportements des uns et des autres vers plus d’égalité.
Ces infrastructures sont définies comme étant des lieux qui façonnent la capacité des
individus à interagir avec les autres, qui favorisent les relations de face à face et qui
soutiennent les liens sociaux. Ils constituent donc des lieux essentiels à la vie publique
et civique.




                                            54
       Concrètement, ce sont les bibliothèques, les équipements sportifs, les centres
communautaires, les espaces culturels (centres, théâtre, salles de concert, etc.), les
marchés, les jardins de jeux, les lieux de créativités (artistiques ou de soutien
professionnel), les espaces de bien-être (piscine, bains publics, etc.) ou encore les lieux
spirituels, les espaces multifonctionnels (107) ( GISSR AMANE (108) pour la prise en charge
des femmes victimes de violences) et les réseaux d’accueil et d’accompagnement à
l’entrepreneuriat dédiés aux femmes. Ces lieux ne sont pas tous explicitement orientés
vers des enjeux de sociabilité, mais leur point commun est de permettre à leurs usagers
de s’y croiser régulièrement.

       Au Maroc, ces infrastructures sont largement héritées à titre d’exemple, les
mosquées, les souks ou les hammams. Au niveau de certaines grandes villes, Rabat par
exemple, ont été développés récemment des espaces sportifs qui ont eu un franc
succès. Cependant, dans leur majorité, les clubs et foyers féminins, et les différentes
déclinaisons de maisons (des jeunes, des femmes, etc.) construits ces vingt dernières
années ne sont pas attractifs et souffrent d’une gestion bureaucrate.

Les facteurs explicatifs à l'origine de la non prise en considération de la mutation de
la famille

       Le lieu commun, largement répandu encore aujourd’hui, selon lequel les
ménages fonctionnent sur la base de la mise en commun des revenus et du principe de
partage indifférencié des ressources, empêche la recherche approfondie sur les
inégalités au sein des couples et fait de ce sujet une zone grise des politiques publiques.
Or, le pouvoir économique et son usage font l’objet de processus complexes de
marquage social (109). Pourtant cette exploration serait salutaire car elle permettrait de
comprendre pourquoi les individus se marient de plus en plus tard ou ne se marient pas,
et pourquoi les femmes décident un jour de quitter leur emploi, même si cela va affecter
négativement le niveau de vie du ménage.

        La répartition des revenus au sein du couple, ou de la famille, est peu abordée
car elle est généralement perçue comme incompatible avec les valeurs de solidarité
familiales, surtout lorsque c’est la femme qui aborde le sujet. Aussi toute discussion à
ce sujet est considérée comme un acte hostile envers la famille, et par extension envers
la religion.

        Les infrastructures existantes souffrent, également, d’un manque de personnel
qualifié pour accompagner la population et répondre à ses attentes. La loi n° 45-18
relative à l’organisation des métiers des travailleurs sociaux a été adoptée en 2021 pour
institutionnaliser le travail social mais la procédure d'accréditation des travailleurs
sociaux est encore en cours d’élaboration.

        Ces métiers sociaux sont généralement assurés par la société civile et sont
insuffisamment encadrés. Ils souffrent encore de manque de consistance, aussi,
souvent ils apparaissent comme des sous-métiers lorsqu’ils devraient mobiliser de
manière puissante les sciences médicales et sociales pour accompagner la population à
participer au vaste chantier de transformation sociale.



                                            55
Les mesures entreprises par les autorités publiques en matière de suivi des mutations
de la famille

        Les mesures sont différenciées. Si la sphère privée du couple est ignorée
(horaires et calendrier scolaires inadaptés, inexistence de cantines scolaires, droit du
travail peu efficient), des mesures ont été mises en place pour accompagner la société
civile depuis 2005, notamment via l’INDH et la construction de bâtiments censés être
autant d’agoras, et renforcer la protection sociale avec la généralisation de la
couverture médicale universelle. Des ajustements sont actuellement débattus
publiquement afin de garantir aux femmes la pleine jouissance de leurs droits de
manière effective.

       La réforme du Code de la famille : l'institution familiale constitue la pierre
angulaire de la stabilité sociale. Le Code de la famille vise à asseoir un modèle de gestion
familiale qui se base sur le partage des responsabilités, durant la vie du couple et après
la rupture. Cependant, même deux décennies après sa mise en œuvre, de nombreuses
discriminations persistent, ce qui alimente une forte résistance au changement dans les
rapports sociaux de genre.

        Depuis la lettre de Sa Majesté le Roi en septembre 2023, une réflexion
approfondie est menée sur la viabilité et la solidité de l'institution familiale au Maroc,
en vue de combler les lacunes existantes dans la garantie des droits complets et
effectifs des femmes. La réforme de ce code est donc attendue pour dépasser les failles
juridiques et les défaillances textuelles, et pour préciser les lectures juridiques et
judiciaires qui ne s’accordent pas avec les transformations de la société et qui ne sont
pas conformes aux principes de la Constitution et des conventions internationales
ratifiées, précisément, le renforcement de la cohésion de la famille, l'intérêt supérieur
de l'enfant, la lutte contre le mariage des mineures, la garantie du transfert des droits
successoraux et l'élimination des discriminations, notamment en ce qui concerne la
tutelle légale et le partage des biens.

        La réflexion autour de la réforme du Code pénal et du Code de procédure Pénale
a été lancée par le Gouvernement en mars 2024, dans l’objectif de mener une réforme
radicale. À cet effet, il y a lieu de souligner l'existence d’interactions structurantes entre
le Code pénal et le Code de la famille pour la protection des femmes, et la nécessité de
prendre en considération le statut pluriel des femmes dans les politiques publiques.
Certaines zones grises du Code Pénal en relation avec la famille nécessitent une
réforme pour relever les nouveaux défis de la société, notamment d’équilibrer l’autorité
parentale, établir la paternité juridique, trouver des solutions pour l’interruption
volontaire de grossesse, abolir les circonstances atténuantes du viol sur mineur.e.s, ou
de criminaliser les crimes technologiques.




                                             56
Les impacts de la non-prise en considération des mutations de la famille

       La démission de la femme du monde économique est le plus grand défi à
dépasser. L’assigner à un espace privé réduit de fait son impact dans la société
puisqu’elle ne peut ni créer, ni contribuer à l’évolution de la société, assignée qu’elle est
à reproduire les actes de survie et de soin aux membres de sa famille, ni produire de la
richesse. La société et l’économie se privent ainsi d’un levier puissant de développement
du pays.

2.3.   Le nœud d’un marché de l’emploi tendu et non-inclusif

        Malgré la dynamique économique observée au cours des vingt dernières années,
la situation de l'emploi des femmes marocaines demeure préoccupante, marquée par
l'étroitesse du marché du travail et son manque d'inclusivité.

       Ce nœud contribue à affaiblir l’émergence d’une classe moyenne et à perpétuer
la vulnérabilité et les inégalités sociales. Les femmes se trouvent souvent confrontées
à des emplois précaires et informels, caractérisés par des salaires bas et des conditions
de travail difficiles. Cette précarité économique limite leur accès aux ressources et
compromet leur autonomie financière, les maintenant dans un cercle vicieux de
dépendance économique. Cette problématique complexe découle de plusieurs nœuds
secondaires, allant de l’étroitesse du marché de l’emploi, au potentiel féminin sous-
exploité et à la carrière professionnelle féminine inexistante.

● Une économie peu diversifiée et peu génératrice d’emplois

       Malgré la croissance économique soutenue enregistrée au début des années
2000, celle-ci n'a pas été accompagnée d'une création d'emplois suffisante pour
absorber la main-d'œuvre disponible. Pendant la période allant de 2000 à 2019,
l'économie marocaine n'a créé en moyenne que 110 000 emplois par an, alors que le
nombre de personnes en âge de travailler a augmenté de 375 000 par an en moyenne
(HCP, 2024).

       De plus, le tissu économique peine à évoluer vers la diversification, l’innovation
et les secteurs à haute valeur ajoutée pour répondre aux besoins d’une société en
mutation et d’un monde en évolution, notamment, en Europe, bassin partenaire
économique traditionnel, et dans les pays du Grand Sud.

       Dans ces conditions, trois alternatives s’offrent aux chercheurs d’emploi en
peine d’intégration : accepter d’entrer dans le marché de l’emploi au prix d’une
dévalorisation sociale, émigrer vers d’autres cieux ou enfin, rester chez soi. C’est cette
dernière alternative qui est la plus souvent choisie par les femmes tant le coût
d’opportunité de travail leur est défavorable.




                                             57
● Une inactivité préoccupante

       Cette création d’emplois limitée, combinée à l'augmentation démographique
persistante, aggrave le taux d'inactivité des femmes. La participation des femmes au
marché du travail est non seulement faible mais ne cesse de baisser, passant de 28,1%
en 2000 à 19% en 2023, un chiffre nettement inférieur à celui des hommes (68% en
2023) (110).

       Ces disparités, accompagnées d'un taux de chômage plus élevé chez les femmes
(18,3% contre 11,5% pour les hommes), d'une concentration de 41,5% de femmes dans
le secteur agricole, et d'une précarité dans l'emploi - où 57% d'entre elles sont des aides
familiales non rémunérées et ne bénéficient pas de protection sociale - renforcent leur
propension à l'inactivité (111). Par conséquent, un grand nombre de femmes, en
particulier dans les milieux ruraux, se retirent du marché du travail ces dernières années,
conséquence de la sécheresse qui a frappé le secteur agricole.
● Un entrepreneuriat féminin limité et axé sur la subsistance

       L'entrepreneuriat féminin peine à s'affirmer comme une alternative efficace pour
l'autonomisation économique des femmes. Celles-ci sont moins enclines à s'engager
dans des activités entrepreneuriales, ne représentant que 3,9% de la population
féminine âgée de 18 ans et plus. En termes de proportion, seulement 22% des
entrepreneurs au Maroc sont des femmes, comparativement à 78% pour les hommes.
En termes qualitatifs, près de 47% des femmes s'engagent dans l'entrepreneuriat par
nécessité, faute à leur incitation à opérer dans le secteur informel (112).
● Une carrière professionnelle peu développée

        Le caractère intermittent des activités professionnelles des femmes, partagées
entre vie professionnelle et vie domestique, les empêche d’envisager leur parcours de
travail en termes de carrière. En effet, l’activité professionnelle des femmes est plus
susceptible d’être interrompue que celle des hommes, hors licenciement, pour des
périodes plus ou moins longues. Ainsi, le mariage et l’arrivée d’enfants constituent des
périodes critiques pour la femme où le degré d’implication dans la vie professionnelle
peut se modifier.

       Tout autant, les accidents de la vie influent directement sur la carrière des
femmes, en cas de prise en charge des parents, d’enfants en situation de handicap ou
d’un entourage immédiat, en cas de vieillesse ou de maladie.

        Dans l’emploi informel, l’instabilité des postes, des activités et des entreprises
fragilisent la carrière des femmes qui n’ont de choix que de suivre le marché.




                                            58
        En général, les femmes accordent plus d’importance à leurs engagements
familiaux qu’à l’évolution de leur carrière professionnelle, certaines font quelques
sacrifices qui ont des répercussions sur leur retraite (113). Par exemple, elles choisissent
de travailler à temps partiel, occupent des emplois précaires ou à durée déterminée (114),
elles prennent des retraites anticipées ou des départs volontaires, elles postulent
rarement pour avoir une responsabilité. Malheureusement, en fin de carrière, elles se
retrouvent face à de faibles retraites. Bien que les statistiques ne soient pas disponibles,
il semblerait que ces mécanismes informels nuisent à leur capacité à accumuler des
droits à retraite et les rendent plus vulnérables dans le système de retraite.

Les facteurs explicatifs à l'origine de ce marché de l’emploi tendu et non inclusif

        Cette situation trouve ses racines dans un enchevêtrement complexe de facteurs
économiques socioculturels, éducatifs et infrastructurels. Sur le plan économique, la
forte dépendance de l'économie marocaine au secteur agricole, exposée aux aléas
climatiques, ainsi que le manque de transformation structurelle et la diversification
insuffisante de ses secteurs productifs, constituent les principaux facteurs limitant la
création d'emplois dans des secteurs émergents et innovants.

         Les pesanteurs des normes sociales discriminatoires et des stéréotypes sociaux
tenaces qui confinent les femmes à des rôles familiaux traditionnels, entravent
considérablement leur engagement sur le marché du travail (OCDE, 2017). L'absence
de mesures d'accompagnement tenant compte des spécificités et des contraintes liées
à l'activité féminine, telles que l'aménagement de l’emploi du temps ou le travail hybride,
a un impact négatif sur leur autonomisation économique.

       Cela affecte également l’opportunité de se lancer dans l’entrepreneuriat en
restreignant l'accès des femmes aux ressources, aux réseaux professionnels et aux
opportunités d'affaires. De plus, le manque d'accès à un appui technique adapté et à
des modèles féminins d'entrepreneuriat réussis limite la confiance et la préparation des
femmes à créer et à gérer une entreprise. En outre, la difficulté à accéder à un
financement suffisant et à des services financiers adaptés constitue un autre facteur
défavorable à l'entrepreneuriat féminin au Maroc.

      Enfin, l'insuffisance des infrastructures publiques de soutien telles que les
crèches ou les moyens de transport disponibles et abordables oblige les femmes
marocaines, tout comme leurs pairs de la région, à jongler entre les exigences
professionnelles et les responsabilités domestiques et familiales.

Les mesures entreprises par les autorités publiques en matière de promotion de
l’autonomisation économique des femmes

        Conscient de ces défis, le Maroc a réalisé des avancées notables dans sa marche
vers l’égalité des genres, en adoptant diverses mesures et initiatives pour encourager
l'autonomisation économique des femmes.




                                            59
       Cette autonomisation est reconnue comme un élément essentiel pour réduire
les écarts entre les zones urbaines et rurales, ainsi qu’entre les différents secteurs
économiques, notamment agricoles et industriels, tout en luttant contre la
discrimination à l'égard des femmes et des filles. Ces initiatives comprennent l'adoption
de normes juridiques favorisant leur autonomisation économique, telles que le statut
général de la fonction publique, le Code du Travail, le Code du commerce, ainsi que
diverses lois relatives à l’accès aux terres collectives (soulaliyates), entre autres.

       En outre, des programmes de soutien à leur intégration économique, comme
l'ICRAM 1 et 2, l'INDH, ont été mis en place. Ces efforts ont été complétés par des
programmes dédiés exclusivement à l’encouragement et au soutien de l’entrepreneuriat
féminin à travers l'appui technique et financier, tels que les programmes Attamkine,
Forsa, Mourafaka, Addaman Ilayki, Min Ajliki, ainsi que par des mécanismes d'aide
sociale destinés aux catégories en situation vulnérable.

       Cependant, la mise en œuvre de ces initiatives a été entravée par la
fragmentation des efforts, le manque de ressources et le besoin d'une plus grande
cohérence et synergie entre les différents acteurs impliqués. De plus, les particularités
observées, tant entre les régions qu'au sein de celles-ci, soulignent que, parallèlement
au développement économique et aux opportunités propres à chaque région, les
normes sociales traditionnelles exercent également une influence majeure sur l’accès
au travail décent et la restriction de l'engagement des femmes sur le marché de l'emploi,
une entrave qui se fait ressentir de manière plus prononcée dans les régions où
l'évolution des structures économiques et sociales est plus lente.

Les impacts inhérents à la faiblesse du marché de l’emploi et à sa fermeture aux
femmes

        Si les défis persistants du marché du travail ne sont pas adressés de manière
structurelle et efficace, les conséquences pourraient être néfastes pour divers aspects
socio-économiques des femmes marocaines. En effet, elles contribuent à perpétuer la
pauvreté et les inégalités sociales, entravant ainsi leur accès à l'éducation, à la santé, au
travail décent et à d'autres services sociaux essentiels. Cette situation peut entraîner
une détérioration de leur état de santé et celui de leur famille, limitant leur capacité à
investir dans l'éducation et le bien-être de leurs enfants.

       De plus, ces inégalités flagrantes alimentent le sentiment d'injustice et les
fractures sociales, créant des tensions potentielles et accentuant le décrochage
volontaire de certaines femmes de la sphère économique et sociale.

        Dans la société, les femmes n’ont pas les mêmes chances que les hommes pour
cumuler une vie active réussie et une vie familiale. C’est pour cette raison que certaines
choisissent de mettre fin à leur carrière. Profitant uniquement des avantages familiaux
et de pensions de réversion quand elles en ont la possibilité, ou souvent aussi de rien,
elles sont obligées de rester cantonnées au rôle d'épouse ou mère où elles bénéficient
des droits dérivés du mari.




                                             60
2.4.   Le nœud de l’iniquité en matière d’accès aux soins et les inégalités sociales de
       santé

        Les inégalités en matière de santé reflètent diverses inégalités sociales. Le terme
"iniquités" est utilisé par l'OMS pour désigner ce concept de "différences dans le domaine
de la santé qui sont inacceptables et potentiellement évitables, mais qui, de plus, sont
considérées comme inéquitables et injustes" (115).

        Selon Adam Wagstaff, ‘’En matière de santé, les pays pauvres tendent à réaliser de
moins bons résultats que les pays les plus riches et, à l’intérieur d’un même pays, les pauvres
se portent moins bien que les riches. Cette association révèle un lien de causalité à double
sens : la pauvreté engendre la mauvaise santé et la mauvaise santé entretient la pauvreté
(116). De même, Thomas Piketty (117), a mis en évidence, au sein des pays avancés, les

liens existants entre l’inégalité, la cohésion sociale, le développement humain et
économique et le ralentissement des rythmes de croissance.

       Le système de santé marocain présente de défis globaux qui le fragilisent. Ces
défis incluent des inégalités d'accès aux soins de santé, les contraintes liées aux
ressources limitées, la faiblesse des infrastructures dans certaines régions rurales, ainsi
que des problèmes de qualité en matière de services de santé fournis dans le cadre de
la couverture universelle de base. Cette situation s’est amplifiée avec l'émergence
croissante de nouvelles crises sanitaires. Selon une enquête du HCP sur l'impact
psychologique de la Covid-19 sur la population marocaine, les femmes cheffes de
ménage ont davantage souffert que leurs homologues masculins, notamment pour ce
qui est de l'anxiété (50,8 % contre 49,1 %), de comportements obsessionnels (33,3 %
contre 23,6 %) et de troubles du sommeil (26,4 % contre 22,9 %) (118).

       A cet effet, il est pertinent d'examiner les sous nœuds relatifs aux inégalités
d'accès aux soins de santé et à la qualité des services médicaux. Cela inclut l'accès inégal
à la couverture sanitaire universelle, les disparités dans les déterminants sociaux de la
santé, les répercussions sur le bien-être et la santé mentale, ainsi que les défis posés
par l'émergence de nouvelles épidémies sanitaires.

● Inégalités d'accès aux soins de santé et qualité des services de santé

       Les inégalités d'accès aux soins de santé représentent des obstacles significatifs
quant à la garantie d’une offre de santé de qualité pour tous. Elles sont multifactorielles,
aggravant les disparités genre, sociales et économiques. Selon l’enquête panel des
ménages réalisée par l’ONDH, en 2017, le taux de consultation médicale parmi la
population en situation de morbidité est passé de 61,7 % en 2015 à 71 % en 2017 (119).




                                              61
       Il est à noter que l'accès aux soins de santé est souvent inégalement réparti au
niveau territorial. Malgré les efforts déployés, les femmes vivant dans des zones rurales
ou reculées rencontrent encore des difficultés pour accéder équitablement aux services
médicaux en raison de la faiblesse des infrastructures médicales, du manque de
personnel professionnels de santé qualifié et des pénuries de fournitures médicales
pouvant compromettre la qualité des soins offerts. D’après les données du Ministère
de la Santé, les régions de Rabat-Salé-Kénitra et Casablanca-Settat accaparent 49% du
nombre total de médecins exerçant dans le public et le privé. Le nombre d’habitants par
médecin dans la région de Drâa-Tafilalet est 3.5 fois plus élevé que celui de la région
de Casablanca-Settat (120). En outre, les coûts élevés des soins de santé constituent
souvent une barrière majeure pour les femmes qui n’ont pas accès aux systèmes de
santé universels.

● Généralisation progressive de la couverture sanitaire universelle

       Depuis le lancement de la réforme de la protection sociale, d'importantes
avancées ont été accomplies dans la progression vers une couverture sanitaire
universelle. Cette extension a touché plus de 10 millions de citoyen.ne.s, avec le
transfert de 4 millions de familles bénéficiaires du régime Ramed vers l'AMO,
permettant d’atteindre un taux d’environ 70,2%.

       Malgré les progrès réalisés et la mise en place de la Couverture Médicale de
Base, la situation demeure inchangée, compromettant ainsi l'accès équitable aux
services de santé. L'offre sanitaire demeure insuffisante et difficilement accessible pour
répondre aux besoins de l'ensemble de la population, notamment pour ce qui est des
femmes inactives ou travaillant dans le secteur informel.

       De plus, le système de santé est confronté à des défis de gouvernance,
caractérisés par des procédures lourdes, quant aux dossiers de prise en charge de
maladies chroniques et de remboursement des frais médicaux. Ainsi, la transition vers
une couverture sanitaire universelle se heurte à des obstacles tels que la réduction des
dépenses directes des ménages et la protection financière de la population contre les
dépenses de santé, ou la demande croissante d'une augmentation et d'une
pérennisation du financement. Selon l'OMS, le Maroc figure parmi les 57 pays du
monde connaissant une grave pénurie de personnel soignant, avec un médecin pour
1370 habitants (121), ce seuil est nécessaire pour atteindre une couverture importante
dans le cadre des interventions essentielles, notamment celles liées à la réalisation des
OMD.

● Inégalités en matière de déterminants sociaux de la santé

       Les inégalités en matière de déterminants sociaux de la santé reflètent les
disparités systématiques. Ces dimensions sont intrinsèquement liées aux situations
vécues dans les domaines de l’éducation, de la santé, du logement et de l’emploi. A ce
propos, trois principaux types d'inégalités en santé peuvent être identifiés : ceux entre
hommes et femmes, entre différentes catégories socio-professionnelles, et entre les
zones rurales et urbaines.



                                           62
       Selon l’étude du MSPS de 2023 (122), en ce qui concerne les visites prénatales, les
indices d’équité horizontale révèlent une iniquité selon le statut socio-économique,
avec une fréquentation plus importante des établissements publics par les femmes
pauvres et des établissements privés par les femmes riches.
       D’abord, certains déterminants immédiats de la santé défavorisent souvent les
femmes par rapport aux hommes, notamment en ce qui concerne les droits à la santé
sexuelle et reproductive, les conditions de travail et la satisfaction professionnelle, ainsi
que pour ce qui est des situations sociales et familiales. Les inégalités de revenus entre
les sexes jouent un rôle crucial, tout comme l'éducation, particulièrement celle des
femmes, qui est liée à de meilleurs choix de santé. Ensuite, ces déterminants sont
également influencés par des facteurs communautaires tels que l'accessibilité
géographique aux services de santé. Les femmes sont souvent désavantagées, en raison
de trajets plus longs et de difficultés d'accès aux infrastructures de santé, ce qui peut
exacerber les inégalités.
       Enfin, cette accessibilité aux soins de santé reste un défi majeur pour les femmes
dans le secteur informel, ayant moins de chances d'être couvertes par une assurance
médicale et au vu de la difficulté de bénéficier des filets sociaux et de couverture
médicale universelle.

● Répercussion des inégalités de santé sur le bien-être et la santé mentale des
  femmes
       Le bien-être et la santé mentale sont des éléments fondamentaux de la santé
globale de la femme. Au Maroc, ni l’état de santé mentale ni le bien-être ne sont
mesurés (123). L'investissement public en santé mentale au Maroc est insuffisant, avec
un nombre limité de lits pour les maladies mentales (2431) et de psychiatres (454), ce
qui témoigne d'un manque d'engagement de l'État dans ce domaine (124).

       L’étude du CESE souligne que la santé mentale est souvent abordée
principalement à travers les troubles mentaux, en négligeant les déterminants
socioculturels et économiques tels que la violence familiale, la discrimination et le
chômage.

        Bien que le système de santé contribue partiellement à la santé mentale (20 à
30%), ces déterminants ont un impact significatif sur le bien-être mental selon la
vulnérabilité individuelle et les risques environnementaux (125). De plus, des lacunes sont
observées en matière de cadre légal et d'expertise judiciaire, ainsi que dans les
procédures d'internement judiciaire en établissement psychiatrique, faute aux capacités
litières et aux infrastructures inadéquates.

        La santé mentale et le bien-être sont étroitement liés, comme en témoigne
l'impact négatif sur le développement de l'enfant en cas de perturbation de la relation
mère-enfant. Les dépressions maternelles pré-, post- et périnatales sont des exemples
significatifs de telles perturbations. Une étude menée au Maroc sur 144 mères a révélé
des taux de prévalence de dépression post-partum de 6,9 %, 11,8 % et 5,6 %
respectivement après 6 semaines, 6 mois et 9 mois. Ces troubles ont des répercussions
importantes sur le bien-être tant des mères que de leurs enfants (126).

                                             63
       De surcroît, il est important de souligner qu’avec la prolifération de l'utilisation
du numérique au quotidien, certaines interactions sociales en ligne ont causé de
nouveaux défis à surmonter qui impactent les femmes. Des phénomènes tels que la
cyberviolence, le cyberharcèlement et le lynchage médiatique représentent des
menaces sérieuses. Ces comportements peuvent avoir des conséquences néfastes sur
la santé mentale et le bien-être des femmes, pouvant se traduire par de l'anxiété, de la
dépression, entre autres conséquences dévastatrices.

● Prévalence de maladies chroniques et épidémiques impactant les femmes

       Les femmes sont confrontées à un certain nombre de maladies chroniques qui
ont un impact significatif sur leur santé et leur bien-être. Parmi les maladies les plus
prévalentes chez les femmes, il y a lieu de citer les maladies cardiovasculaires, les
problèmes de fertilité, l'hypertension artérielle, le cholestérol élevé, le diabète, les
cancers (du sein, du col de l'utérus, de l'ovaire et le colorectal), les maladies respiratoires
chroniques (l'asthme et la bronchopneumopathie chronique obstructive) et les troubles
mentaux (la dépression et l'anxiété).

       Par ailleurs, l'émergence de nouvelles épidémies sanitaires représente une grave
préoccupation pour la santé mondiale des femmes. Selon une enquête du HCP sur
l'impact du coronavirus, la crise sanitaire a exacerbé les inégalités, affectant davantage
les familles dirigées par des femmes que celles dirigées par des hommes.

        Les facteurs sociodémographiques ont mis en lumière des disparités
importantes, notamment en ce qui concerne l'accès aux soins de santé reproductive, où
l'écart est considérable entre les femmes vivant en milieu urbain (100%) et celles vivant
en milieu rural (17,3%), ainsi que pour ce qui est des hommes en milieu rural (63,4%).

       Pendant la période de confinement, l'accès aux services de santé a diminué de
45%, touchant plus durement les femmes et les hommes vivants en milieu rural
(respectivement 53,1% et 45,9% pour les maladies chroniques et 41,2% et 33% pour
les maladies temporaires) que leurs homologues urbains. (HCP 2022)

Les facteurs explicatifs de l’iniquité en matière d’accès aux soins et les inégalités
sociales de santé

       Les iniquités en matière d'accès aux soins de santé et les inégalités sociales de
santé sont souvent le résultat de multiples facteurs interconnectés, où les femmes
défavorisées ont généralement un accès plus limité aux soins de santé en raison de
contraintes financières, d'un manque de couverture médicale et de ressources limitées
pour se rendre aux établissements de santé à cause des barrières géographiques.

       De plus, les iniquités linguistiques et culturelles peuvent entraver l'accès aux
soins aux femmes, en raison de la méconnaissance des services disponibles pour ce qui
est de la communication avec les prestataires de soins. Ces inégalités peuvent
également avoir des conséquences économiques et sociales importantes, pesant
lourdement sur les femmes, les familles et les systèmes de santé.




                                              64
Les mesures entreprises par les autorités publiques en matière d’accès à la santé

       Au cours des dernières décennies, le Maroc a mis en place diverses stratégies et
programmes visant à agir sur les déterminants de la santé afin d'améliorer le bien-être
des femmes, des mères et des enfants, tout en réduisant les disparités régionales et les
iniquités en matière de santé. Ces initiatives ont eu pour objectif de réduire la mortalité
maternelle et infantile, en mettant l'accent sur les zones rurales, d'étendre la couverture
médicale, de promouvoir la planification familiale, la gratuité des accouchements, la
vaccination, la nutrition, la prévention et l'accès aux soins. Parmi ces stratégies, il y a
lieu de citer les plus importantes notamment :

•   Les 2 plans de stratégies sectorielles couvrant les périodes 2008-2012 et 2012-
    2016 ;

•   Le Plan Santé 2025 axé sur l’amélioration des soins hospitaliers et le développement
    des programmes de prévention contre les maladies en milieu urbain et rural, pour les
    populations à accès difficile (127) ;

•   Le Programme national de prise en charge des femmes et des enfants victimes de
    violences (128) adopté en 2017, intégrant une dimension préventive et sociale pour la
    lutte contre toutes les formes de violence à l’encontre des femmes, et apte à
    améliorer les services de prise en charge FVV ;

•   Le programme d’appui à l’accès inclusif aux infrastructures de santé adopté en 2020,
    visant à améliorer l’accès aux services de santé et aux prestations sanitaires pour
    réduire les disparités dans les régions enclavées (129) ;

•   La Stratégie Nationale de la Santé Sexuelle et Reproductive, adoptée en 2021,
    préconisant l’amélioration de l’accès des femmes et des filles aux services de la SSR
    de qualité (130) ;

•   Le programme d’appui à l’accès inclusif aux infrastructures de santé adopté en
    2020, préconisant l’amélioration de l’accès aux services de santé et aux prestations
    sanitaires pour la réduction des disparités aux FFVV dans les régions enclavées (131) ;

•   La 2ème Stratégie Nationale de la Santé des Adolescents et des Jeunes 2022-2030
    adoptée en 2023, qui vise à développer une offre de services égalitaire, de qualité,
    efficace, adaptée et centrée sur les adolescent.e.s et les jeunes (132).

        Par ailleurs, la réforme de la protection sociale lancée en 2021 par Sa Majesté le
Roi Mohammed VI a considérablement renforcé le corpus juridique en matière de santé.
En adoptant la loi cadre n° 9-21 sur la protection sociale en 2021, cette réforme basée
sur le principe de non-discrimination pour assurer une inclusivité maximale, préconise
la généralisation de la couverture sociale, des allocations familiales, de la retraite et de
l'indemnité pour perte d'emploi.



                                            65
       Pour parachever la réforme entamée en 2001, elle a été amorcée par l’adoption
de la loi n° 65-00 instaurant l'Assurance Maladie Obligatoire pour les salariés des
secteurs public et privé (133). Cette loi a étendu progressivement la couverture médicale
de base et contribué à la lutte contre les disparités régionales et socio-économiques en
matière d'accès aux soins de santé.

        Cet élan de réformes a continué avec l’adoption en 2022 de la loi-cadre 06.22,
illustrant une approche pluridimensionnelle pour généraliser la protection sociale et
garantir l'accessibilité des femmes à une offre de santé de qualité. Cette loi passe par
l’adoption d’une bonne gouvernance, la valorisation des ressources humaines, la mise à
niveau de l’offre sanitaire et la digitalisation de tout le système de santé. Elle prévoit
aussi la création d’une Agence des médicaments et des produits de santé, et d’une
Agence du sang et de produits dérivés du sang (projet de loi 10-22).

        Concernant la valorisation des ressources humaines, une nouvelle loi n° 09.22
sur la fonction publique sanitaire a été élaborée, en vue de motiver le capital humain
dans le secteur public, réduire le manque actuel en ressources humaines, réformer le
système de formation. Sans oublier l’ouverture sur les compétences médicales
étrangères, et l’encouragement des cadres médicaux marocains résidant à l’étranger à
retourner exercer au Maroc (134).

        En dépit des réformes entreprises, le secteur de la santé est confronté à divers
défis. D'une part, à des défis structurels persistent tels que le besoin de renforcer la
gouvernance, de valoriser les professionnels de la santé, de moderniser l'offre sanitaire
au niveau territorial et de la numériser, ainsi que d'améliorer l'accès aux droits en
matière de santé sexuelle et reproductive, en plus de défis émergents liés aux épidémies
et à la prise en charge des problèmes de santé mentale.

       D’autre part, la réforme en cours fait face aux défis relatifs de généralisation de
la couverture médicale et de la protection financière adéquate pour tous les
citoyen.ne.s, y compris ceux œuvrant dans le secteur informel. Il est également essentiel
de renforcer la prévention et l'accès à des services de qualité et de proximité, en
mettant l'accent sur les droits et le genre. De plus, il est crucial d'améliorer la
disponibilité des médicaments (135) et la mise en place d’un système d’information
sanitaire intégré, digitalisé, axé sur le patient avec un identifiant unique et accessible de
prise en charge médicale, de gestion et de gouvernance à tous les niveaux.

Les impacts de l’iniquité en matière d’accès aux soins et les inégalités sociales de santé

        Les iniquités en matière d'accès aux soins et les inégalités sociales de santé sont
des problèmes majeurs qui compromettent le bien-être de femmes. Tout d'abord,
l'iniquité dans l'accès aux soins de santé crée un fossé entre les citoyennes aptes à
bénéficier des services de santé et celles qui ne le peuvent pas. Cette disparité peut
être due à divers facteurs tels que le statut socio-économique, le lieu de résidence. Les
femmes qui ont un accès limité aux soins de santé sont plus susceptibles de subir des
incidences graves sur leur santé, car elles ne peuvent bénéficier de services préventifs,
de traitements appropriés ou des suivis médicaux nécessaires.




                                             66
       Ces inégalités sociales de santé exacerbent les disparités existantes en matière
de santé, de déterminants sociaux tels que le revenu, l'éducation, le logement, l'emploi
et l'appartenance géographique. Toutes ces inégalités sociales contribuent à la
perpétuation d'un cercle vicieux. Les femmes défavorisées sur le plan social et
économique se retrouvent confrontées à un risque accru de maladies, de handicaps et
de décès prématurés, alimentant ainsi un cycle de désavantage et de vulnérabilité.

       Au niveau sociétal, ces inégalités peuvent entraîner une perte de productivité
économique due à des maladies évitables et à des incapacités prématurées, ainsi qu'à
une augmentation des coûts des systèmes de santé publique. Les individus et les
familles confrontés à des difficultés d'accès aux soins de santé peuvent également faire
face à des coûts financiers élevés liés aux traitements médicaux, ce qui peut entraîner
une détérioration de leur situation économique et leur maintien sous le seuil de
pauvreté.

2.5.   Le nœud des systèmes de gouvernance caractérisés par le déficit en termes
       d'égalité de genre et de parité

       La participation égalitaire des femmes dans les systèmes de gouvernance, qu’ils
soient institutionnels, politiques ou économiques, est de nature à favoriser une
meilleure prise en compte des besoins genrés et créer les conditions d’un
développement inclusif optimal.

       Au Maroc, le déficit en termes d'égalité et de parité de genre au niveau de la
gouvernance constitue un véritable nœud pour le développement harmonieux et
intégré du pays. Il relève de plusieurs facteurs dont la faible participation des femmes
dans les postes de décision politiques, institutionnels et économiques, le manque
d’implication dans l’élaboration des politiques publiques, les mentalités réfractaires au
changement qui caractérisent le fonctionnement des partis politiques, et l’ineffectivité
du droit constitutionnel à la parité.

•   Une faible présence dans la prise de décision institutionnelle, politique et
    économique

       La participation politique et institutionnelle des femmes a connu une évolution
positive depuis 2002 de par la présence accrue des femmes dans les instances élues
nationales, locales et régionales, au sein du gouvernement et des conseils
constitutionnels, des partis politiques et des syndicats, et dans l’administration
publique. Le taux de participation peine toutefois à atteindre ne serait-ce que le niveau
du tiers requis pour peser sur les décisions. Il demeure également loin de représenter
une force réelle, les femmes étant sous représentées aux niveaux décisionnels, ce qui
ne leur permet pas de détenir un pouvoir réel dans ces sphères, étant plus dans une
posture de suivisme que de leadership.

       Parallèlement, le plafond de verre s’est certes quelque peu déplacé dans les
entreprises où les femmes commencent à investir, quoique de manière timide, les
hautes fonctions dirigeantes. Cela demeure toutefois insuffisant pour créer les
conditions de dynamisation de leurs performances.


                                           67
•   La voix des femmes inaudible dans les politiques publiques

       La marginalisation de la moitié de la population de la contribution égalitaire aux
centres de décision politiques et institutionnels rend par ailleurs leur voix inaudible dans
la conception des politiques publiques, privant celles-ci d’une approche plus ouverte,
plus créatrice et plus inclusive dans leur élaboration et leur mise en œuvre.

•   Un champ politique réfractaire aux changements

       Les partis politiques, et également les syndicats, véhiculent en effet
généralement une conception traditionaliste du pouvoir plutôt qu’une valorisation des
compétences et du débat d’idées. Ils reposent sur des modes de fonctionnement peu
démocratiques qui ne favorisent pas de réelles dynamiques de changement et
d’évolution des mentalités.
       Dans un tel contexte, ils sont plus enclins à la reproduction de schémas culturels
et de stéréotypes de genre, en particulier sur la place des femmes dans la hiérarchie
interne du pouvoir ainsi que dans la vie publique. Une telle situation est génératrice de
comportements discriminatoires accompagnés souvent de formes de violence qui
écartent les femmes des mécanismes de pouvoir.

•   L’ineffectivité de la parité représentative

        Le champ politique demeure ainsi réfractaire à la prise en compte des principes
d’égalité et de parité. Cette situation est amplifiée par l’ineffectivité du droit à l’égalité
et à la parité, inscrit depuis 2011 dans la Constitution, qui constitue une avancée
fondamentale dans la reconnaissance de la place de la femme dans la société.

Les facteurs explicatifs à l'origine de la faible participation des femmes aux systèmes
de gouvernance

       Parmi les facteurs explicatifs de ce nœud, outre les dysfonctionnements qui
caractérisent le système de gouvernance global, figurent :

● La persistance de résistances sociales liées aux mentalités et aux stéréotypes en
  l’absence d’une stratégie globale de transformation culturelle de la société fondée
  sur la culture de l’égalité et du respect des droits fondamentaux.

● La faible pénétration de la culture démocratique, socle de renouvellement de la
  pensée politique et sociale et des modes d’expression de la diversité et du partage,
  qui seraient aptes à faire évoluer la réflexion et les pratiques.

● L’absence d’une stratégie globale intégrée en matière d’égalité et de parité qui aurait
  pu permettre la mise en œuvre des dispositions avancées de la Constitution.




                                             68
● L’insuffisante prise de conscience par les entreprises de l’importance de l’égalité et
  de la parité en tant que facteurs de performance. En effet, selon plusieurs études, la
  diversité de genre au sein des entreprises est à l’origine d’une diversité de
  comportements qui impacte positivement la performance et les résultats
  économiques (diversité des compétences, augmentation de la qualité de la
  composition des équipes et de leur créativité). L’égalité de genre en tant que valeur
  constitue en ce sens un levier de cohésion interne et de développement des
  capacités des entreprises et donc de leurs opportunités de croissance. A titre
  d’exemple, selon le rapport de l’Organisation Internationale du Travail (OIT) de 2019,
  près de trois quarts des groupes favorisant la parité dans le management constatent
  une hausse de leurs bénéfices allant de 5 à 20 %. L’étude de Deloitte « Diversité et
  inclusion : comment faire de l’inclusion un levier de transformation des organisations »
  dévoile par ailleurs que les entreprises dotées de politiques d’égalité et de mixité
  voient leurs chances d’augmentation de leurs profits et de leur productivité croître
  de près de 60 % (136).

Les mesures entreprises par les autorités publiques en matière d’encouragement à la
participation féminine aux systèmes de gouvernance

Plusieurs réformes et politiques publiques ont été entreprises pour résorber le déficit
de gouvernance dans le domaine de la participation des femmes à la vie publique,
développé dans le premier chapitre de l’étude. Parmi les plus importantes :

● La réforme de la Constitution du Royaume en juillet 2011 qui a consacré plusieurs
  dispositions aux principes d’égalité et de parité ;

● L’adoption de la loi organique 02-12 relative aux nominations aux emplois supérieurs
  qui encourage la mise en œuvre de la parité dans les postes de décision ;

● Les agendas gouvernementaux pour l’égalité visant à garantir l’accès des femmes aux
  postes de décision dans l’administration publique et dans le domaine de
  l’autonomisation économique et sociale ;

● La mise en place de mesures de discrimination positive dans le domaine de la
  démocratie représentative, qui ont progressivement évolué depuis l’instauration de
  la liste nationale en 2002 ;

● L’introduction du quota dans les instances des partis politiques ;

● Le renforcement, depuis juillet 2021, de la diversité de genre dans les organes
  d’administration et de contrôle des sociétés anonymes.

Ces chantiers ont généré des acquis non négligeables en termes de renforcement de la
visibilité des femmes dans les processus décisionnels, sans toutefois pouvoir
transformer de manière effective et durable le caractère masculin du pouvoir.




                                            69
  Les impacts du déficit de participation des femmes aux systèmes de gouvernance.

         La persistance de ces déficits de gouvernance priverait le pays d’un potentiel
  essentiel dans sa quête de développement. Ce qui risque à terme de compromettre, ou
  à tout le moins de ralentir sérieusement, les dynamiques positives de création de
  richesses, de renforcement de la cohésion sociale et, aussi, de consolidation de l'image
  du pays à l’international.

  Chapitre 5. Scénarios du futur : de nouveaux horizons à explorer pour les
              femmes
         Les tendances longues de l’évolution sociale du Maroc, ainsi que ses mutations
  conjuguées au développement économique du pays, et plus récemment
  géostratégique, interrogent l’évolution à venir sur la position de la femme marocaine
  dans sa société.

         D’une part, il est indéniable que tous les indicateurs de développement
  soulignent la nécessité de renforcer les capacités des femmes et de les inclure
  davantage dans les sphères économique et politique, reconnaissant ainsi le potentiel
  transformateur inhérent à cette démarche. De ce point de vue, le Maroc, en se privant
  d’une partie de sa population, se condamne à un développement incertain, ou tout du
  moins versatile.

         D’un autre côté, la vitesse des changements sociétaux crée une impression de
  manque de maîtrise de la situation, alimentant une crainte de l’avenir. Face à un monde
  en évolution constante dont les soubresauts impactent rapidement jusqu’au quotidien
  des individus, le sentiment d’incertitude, d’anxiété sociale et l’impression d’inconfort
  prennent souvent le dessus, et l’attitude attentiste devient la norme. Pourtant, tous les
  ingrédients sont là pour assurer une prospérité durable à l’ensemble de sa population.
  De ces constats, deux scénarios ont été développés : un scénario tendanciel et un
  scénario souhaitable.

1. Le scénario tendanciel à l'horizon 2050, un regard vers demain

 1.1.       Le scénario tendanciel de la femme marocaine esquisse une trajectoire basée sur
            les tendances actuelles et les évolutions observées

        ●    Une polarisation de la société accentuée

         Même si la réforme de l'éducation-formation 2015-2030 et sa continuité ont été
  très ambitieuses, le fond de la problématique de l'éducation n'a pu être modifié en
  profondeur du fait de fortes résistances des acteurs du système interne (acteurs du
  système éducatif) et externe (dont les familles et les acteurs politiques et économiques).
  Les savoirs acquis en classe ne permettent pas l'autonomisation de l'individu et le
  développement de son sens critique nécessaires pour que la personne puisse s'adapter
  à un monde en constant changement.




                                               70
       Aussi, l’école reste, en général, le lieu par excellence de reproduction des
stéréotypes de genre. Plus qu’avant, il n’y a pas un mais au moins deux Maroc : celui
minoritaire de la prospérité, du bien-être et de l’abondance, et celui majoritaire de
l’austérité, de la résilience et du conservatisme. La polarisation de la société s’accentue
entre ceux qui sont ancrés à l’économie-monde et ceux qui ont décroché par conviction
ou faute de moyens. Les inégalités sociales s’accentuent très fortement du fait d’un
ascenseur social en panne.

    ●   Une autonomisation économique féminine précaire

        En l'absence d'une réelle convergence entre les stratégies nationales de l'emploi
et les initiatives sectorielles, la situation des femmes marocaines sur le marché du travail
reste précaire et peu propice à leur autonomisation économique. Les politiques mises
en place n'ont pas eu l'impact escompté, laissant les femmes confrontées à des
obstacles persistants dans leur accès à l'emploi et à des opportunités économiques
équitables.

        L'espoir d'un sursaut économique stimulé par l'organisation de la Coupe du
Monde de Football en 2030, en partenariat avec l'Espagne et le Portugal, a été déçu.
Cet événement, s’il a constitué une opportunité pour certains secteurs, n'a pas eu
d’effet diffus de modernisation et de dynamisation sur l'ensemble de l’économie du
pays. Son impact aura été limité, ne parvenant pas à stimuler de manière significative
les activités productives, ni à favoriser l'autonomisation économique des femmes.

        Dans ce contexte économique, les pressions démographiques continuent de
s'exercer avec vigueur. À l'horizon 2050, la population en âge d'activité devrait
augmenter de 8 millions de personnes, dont la moitié serait constituée de femmes.
Selon les simulations effectuées, prenant en considération la baisse tendancielle du taux
d'activité féminin, le nombre de femmes inactives augmenterait de 5,2 millions, portant
leur total à 16,2 millions en 2050. Ces pressions demeureront significatives même avec
un scénario de taux d'inactivité constant, avec une augmentation prévue de 3,2 millions
de femmes inactives, portant leur nombre à 14,2 millions (137).

       Ainsi, les opportunités d'emploi restent limitées, les écarts salariaux persistent et
les femmes demeurent sous-représentées dans les secteurs économiques clés. Sans
une action décisive et coordonnée, leur autonomisation économique risque de
demeurer un objectif lointain, laissant le potentiel économique et social des femmes
largement sous-exploité.

       Ce manque de perspectives accélère l’émigration féminine, mais là encore, faute
de considérer le phénomène dans sa globalité, les externalités positives de ce
mouvement sont sous-exploitées et ne font qu'augmenter le cercle vicieux de la
dépendance des femmes. Cette dépendance est accentuée par le manque de
discernement, face à la dégradation des ressources naturelles et les conséquences des
changements climatiques sur la situation des femmes encore considérées, notamment
en période de crise (Covid 19 par exemple). À la charge mentale liée à la gestion
domestique s’ajoute celle des conséquences de la sécheresse et du stress hydrique.




                                            71
    ●   Un lien social fragilisé

        La poursuite de l'éducation, l'émergence de carrières professionnelles, la
frustration à ne pas accéder à un travail décent, les changements sociaux et les
ambitions individuelles font que la femme aspire à un changement profond dans la
nature des liens familiaux. Certes, ces derniers connaissent des tensions causées par le
stress, la charge mentale de la femme, l'individualisme, le désir d'épanouissement
personnel, de réussite financière et de reconnaissance sociétale. Cependant, face à une
situation où les personnes sont confrontées à un monde en constante évolution, la
famille reste le refuge par excellence, malgré ses équilibres précaires. Ainsi, même si le
maintien des liens sociaux a un coût que la vie moderne ne permet plus, la généralisation
de la protection sociale et l'investissement dans la solidarité intra-familiale reste le
meilleur filet social.

        Il est néanmoins important de souligner la prégnance du sentiment de frustration
accumulée chez les femmes. Ce dernier pourrait être la cause d’un mal-être général, qui
ne concerne pas seulement les femmes, et qui provoque une recrudescence de
maladies, notamment mentales, mais aussi chroniques. Les frictions sociales alimentent
également la violence à l’égard des femmes qui reste insuffisamment encadrée par le
circuit de prise en charge et par la loi.

        Résolument ancrées dans un système monde, physiquement parce qu’elles
voyagent pour les loisirs, le travail ou les études, imaginairement parce qu’elles utilisent
les moyens de communication virtuels dont les réseaux sociaux, leur responsabilité dans
l’entretien et le maintien des liens pèse lourd face à leurs désirs de s’épanouir. Ce poids
est d’autant plus lourd que l'État social mis en place ne permet pas de combler tous les
aspects de la solidarité sociale. La transition d’une société basée sur les solidarités
mécaniques aux solidarités organiques se fait difficilement et lentement, en partie parce
que le tissu économique ne suit pas l’évolution démographique.

    ●    Un accès non équitable au système de santé qui accentue les inégalités

       En l'absence d'une véritable convergence des stratégies nationales de santé et
des initiatives sectorielles et de politiques sanitaires adaptées aux besoins de la
population, l'accès des femmes marocaines à des soins de santé de qualité et à leurs
droits en matière de santé sexuelle et reproductive demeure précaire, compromettant
leur autonomisation économique.

        Le secteur de la santé fait ainsi face difficilement à de nombreux défis structurels
persistants liés à une gouvernance lâche, à une offre sanitaire insuffisante au niveau
territorial et à un accès inégal aux droits en matière de santé sexuelle et reproductive,
qui impactent négativement les femmes. En outre, de nouveaux défis émergent liés aux
nouvelles épidémies, aux troubles de santé mentale, à la gériatrie, à la procréation
médicalement assistée (PMA) ainsi qu’à la généralisation des nouvelles méthodes
contraceptives. Par ailleurs, les politiques de santé continuent d’aborder
insuffisamment la ménopause et les problèmes qui en découlent, en termes de
prévention et de prise en charge des morbidités associées à cette phase de vie.




                                            72
     ●   Un système de gouvernance qui reste résolument patriarcal

        Le cadre normatif évolue lentement sans mesures impactantes sur la présence
 des femmes dans les différentes sphères de décision. L’Autorité pour la Parité et la Lutte
 contre toute forme de Discrimination et le Conseil Consultatif de la Famille et de
 l'Enfance n'ayant pas été mis en place, le suivi de l’évolution du cadre juridique n’a pas
 été rendu opérationnel, les différents acteurs concernés n’ayant pas été suffisamment
 impliqués.

        En conséquence, la présence des femmes atteint en 2050 péniblement 30% dans
 certaines sphères. La crise des structures organisationnelles partisanes qui a été révélée
 en 2011 a perduré dans le temps sans qu’une solution durable n’ait été trouvée pour
 pousser les citoyen.ne.s à s’engager politiquement. De fait, le renouvellement des
 candidats aux postes d’élection se fait au rythme des rendez-vous électoraux et des
 réseaux de cooptation.

         Dans les instances décisionnelles de l’Etat (assemblées élues, gouvernement,
 collectivités territoriales), les femmes ne sont toujours pas intégrées de manière
 optimale et restent cantonnées à des rôles subalternes. De la même manière, la fonction
 publique continue de ne favoriser que peu l'accès des femmes aux postes de
 responsabilités. Seul le secteur privé a continué de favoriser l’accès des femmes aux
 postes stratégiques, du fait notamment de l’ouverture économique du pays vers
 l’international.

2. Les leviers de changement pour impulser un nouvel élan

        L'horizon des femmes au Maroc est plein de promesses, d'opportunités et de
 signaux de changement qui laissent présager la transformation des réalités et le choix
 d’une société plus équitable et inclusive. En effet, certains facteurs se présentent
 comme des leviers puissants pour l'autonomisation féminine aussi bien sociale
 qu’économique, ouvrant des voies diversifiées vers des carrières qui transcendent les
 frontières traditionnelles de genre.

        Cette conjonction d'éléments offre aux femmes marocaines l'opportunité unique
 de jouer un rôle actif et influent dans des domaines qui étaient autrefois dominés par
 les hommes. Des perspectives de carrière variées vont s'ouvrir, propulsant les femmes
 vers des secteurs tels que la technologie, l'entrepreneuriat innovant, le sport (le football)
 et dans d'autres domaines innovants, élargissant ainsi les possibilités qui s'offrent à
 elles.

         Les germes de changement sont façonnés par des opportunités croissantes, à
 travers la prise en compte de nouvelles manières d’être au monde par les jeunes
 générations, mais aussi l’intégration du Maroc dans l'économie mondiale pouvant créer
 des opportunités économiques diversifiées pour les femmes, des changements culturels
 positifs et une participation accrue des femmes dans divers secteurs de la société. Ces
 germes de changement démontrent le potentiel caché d'une transformation culturelle
 et économique significative, où les femmes sont potentiellement une force motrice qui
 contribuera de manière significative au développement économique et social du pays.


                                              73
    ●   Changements dans les comportements des femmes

        Les femmes de 2050 s'affirmeront plus sans complexes et n’accepteront plus de
composer avec des pratiques ou des comportements inspirés d’une tradition imaginée.
Les tendances de fond sont repérables dans la vie quotidienne des femmes.
L’individualisation de l’habitat du couple, par rapport à la grande maison familiale, et son
équipement en sont des exemples.

        Corrélé à cela, la montée d’un encadrement plus individualisé des enfants, que
certains observateurs qualifient de montée de l’enfant-roi, bouleverse les relations de
couple et entre générations. Une certaine distance des relations entre parents et
enfants d’une part, et entre la femme et la gestion de son foyer et la répartition inégale
des tâches non rémunérées d’autre part se fait sentir à la double faveur de la vie urbaine
et de la transformation des moyens de communication.

       Ce dernier point en particulier constitue un puissant germe de changement et
accélérateur de transformations. La génération Alpha est formée par les enfants nés
après 2010. Ils auront donc 40 ans en 2050. Cette nouvelle génération est
particulièrement exposée aux nouvelles technologies : elle n'a pas vraiment connu de
monde hors ligne et sans réseaux sociaux. Ces jeunes filles et garçons sont familiarisés
depuis leur naissance avec les appareils intelligents et connectés que ce soit
directement ou par procuration. Ils ont donc une compréhension particulière des
relations sociales, investis intimement de manière décomplexée dans les échanges tout
en gardant suffisamment de distance pour rompre avec ce qui ne leur convient plus.

       Le numérique fait partie de leur quotidien. En plus d'être hyperconnectée, la
génération Alpha est également créative. Elle s’investit dans la recherche de
divertissement et de nouvelles connaissances, et se distingue aussi par sa sensibilité aux
causes environnementales et à la protection des animaux. Elle est attirée par la justice
climatique et sociale, l'authenticité et l'expérience unique. Elle a donc tendance à être
plus rapide et radicale dans ses choix, avec un fort tropisme pour la protection du
monde dans lequel elle vit. S’affranchissant des règles convenues de socialisation, ces
jeunes seront plus enclins à abandonner certaines logiques de perpétuation des
inégalités de genre.

    ●   Nouvelles technologies et intelligence artificielle

         L'instauration d'un accès démocratisé aux nouvelles technologies et à
l'intelligence artificielle (IA) offre des perspectives prometteuses pour l'amélioration de
la condition des femmes au Maroc parce qu’elles permettront un accès direct à
l’information sans intermédiaire, donc sans tutelle. Sur le plan éducatif, les supports
pédagogiques en ligne surmontent les barrières géographiques et socio-économiques,
permettant un accès facilité des femmes aux formations, favorisant ainsi l'acquisition
de compétences pratiques et techniques essentielles, qu’il s’agisse d’éducation juridique
ou de compétences liées aux exigences en constante évolution du marché de l'emploi
par exemple. Il est aisé, dans cette même perspective d’imaginer que les fonctions
d’accompagnement administratif à la personne soient prises en charge par l’intelligence
artificielle et l’automatisation.


                                            74
       Parallèlement,       les    technologies     numériques     facilitent    l'initiative
entrepreneuriale, offrant aux femmes l’opportunité d'accéder aux réseaux et aux
marchés, qu'ils soient locaux ou internationaux. Cette facilité résulte de la possibilité de
créer des clusters économiques, de commercialiser en ligne leurs produits ou services,
élargissant ainsi leur clientèle et renforçant leur autonomie économique.

        De plus, les applications basées sur l'IA apportent des solutions novatrices aux
défis rencontrés par les entrepreneures, ouvrant la voie à une transformation
significative du paysage entrepreneurial féminin. En outre, ces avancées technologiques
offrent des modèles de travail flexibles, notamment le travail à distance, ou en mode
hybride. S’il est certain que les nouvelles technologies vont détruire certains emplois
déjà existants, elles vont également permettre aux femmes d’atteindre de nouveaux
domaines jusqu’alors inaccessibles, débarrassées des actes de gestion banals,
automatisés et mécaniques.

        Hors monde éducatif et professionnel, les nouvelles technologies servent
également à faciliter la vie quotidienne des familles grâce au développement et à la
démocratisation de la robotisation, de l’automatisation et de la domotique, déchargeant
ainsi la femme de nombreuses tâches quotidiennes pénibles.

        Dans un domaine plus spécialisé, la télémédecine peut contribuer à transformer
de manière significative le secteur de la santé, notamment pour les spécialités médicales
très pointues ou encore dans les zones rurales les plus éloignées. Cependant, il est
essentiel de prendre conscience que l'accroissement de l'utilisation de l'intelligence
artificielle dans ces secteurs entraîne également des risques, en particulier sur le plan
éthique, notamment la cybercriminalité et les nouvelles formes de discrimination dans
le numérique, la manipulation des "deep fakes" et les attaques cyber-physiques.

       Les préoccupations éthiques liées à la confidentialité des mégadonnées, à la
sécurité de la vie privée et la confidentialité, à la dépendance technologique et à la
possible substitution des interactions humaines, doivent être minutieusement évaluées
et encadrées afin de garantir un impact positif sur la vie quotidienne des femmes.

    ●   Ouverture du Maroc au monde

       La confrontation à l’autre a toujours été porteuse d’un double mouvement de
renforcement identitaire et de fructification des échanges. Dans ce cadre, elle poussera
la femme marocaine à redécouvrir et renforcer son identité dans le cadre d’un monde
qui ne demande qu’à être conquis par elle.

        Le Maroc a opté, depuis son indépendance, pour un scénario d’ouverture sur son
environnement régional et international. Ce choix, qui s’inscrit dans la continuité de son
histoire, s’explique par sa position géostratégique de confluence entre l’Europe et
l’Afrique, d’appartenance à l’espace méditerranéen ainsi que par l’étendue de ses
façades maritimes, tant méditerranéenne qu’atlantique, qui le prédestinent à devenir un
hub régional d’envergure, un aspect que le pays revendique et sur la base duquel il a
assis ses relations politiques, économiques et culturelles, bilatérales et multilatérales.




                                             75
         Cette orientation stratégique a été une nouvelle fois consolidée par la Volonté
 Royale, présentée lors du Discours du Souverain à l’occasion de la célébration du 48ème
 anniversaire de la marche verte, le 6 novembre 2023, via la création d’un espace partagé
 de rayonnement, de paix et de prospérité, englobant les pays de la côte atlantique de
 l’Afrique pour créer un corridor économique reliant l’Afrique atlantique aux
 hémisphères nord et ouest, en plus de favoriser l’accès des pays du Sahel à cet espace
 maritime. Cette nouvelle orientation s’ajoute aux autres axes stratégiques d’ouverture
 au monde. Si le tropisme africain du Maroc n’est plus à démontrer, l’Asie n’est pas en
 reste puisque le Maroc a multiplié les accords, notamment commerciaux et
 économiques, avec les pays de cette zone du monde, devenant un partenaire de
 dialogue sectoriel avec l’ASEAN (association des Nations d’Asie du Sud-est).

         Cette ouverture voulue va accélérer l’évolution du statut de la femme. Aussi,
 l’intégration des femmes dans cette dynamique serait porteuse de nouvelles
 opportunités d’autonomisation et d’émancipation économique et sociale, via les
 opportunités économiques, sportives mais aussi les migrations pour études ou emploi,
 qui modifieraient considérablement leur avenir. Le cas contraire serait de nature à
 renforcer leur marginalisation, notamment du marché du travail et de la dynamique
 sociale.

3. Le scénario d’un futur raisonné pour la femme marocaine

         Le scénario d'un futur raisonné se distingue par la continuité des tendances de
 changement amorcées d'ici à 2050, confirmant ainsi l'orientation du Maroc vers une
 ouverture au monde et une adhésion aux grandes valeurs universelles. Ce scénario offre
 des perspectives favorables pour améliorer la condition des femmes au Maroc dans
 l’avenir.

       La perspective d'un avenir souhaitable pour le Maroc repose sur le dépassement
 des retards enregistrés et les défis émergents ainsi que sur l'exploitation des
 opportunités pour améliorer la condition des femmes.

        En tenant compte des aspirations exprimées dans les Discours Royaux et des
 besoins du pays, cet avenir se fonde sur les quatre nœuds leviers présentés
 notamment : la culture égalitaire, la famille équilibrée, la gouvernance partagée et
 l’emploi inclusif. Il vise à consolider la démocratie, à réduire les inégalités systémiques
 en prenant en considération les transformations sociétales et leur impact sur la
 condition des femmes. Il s'appuie également sur des germes de changement,
 notamment, l’intégration des nouvelles technologies et l’intelligence artificielle,
 l’ouverture du Maroc au monde et les changements dans les pratiques des femmes. Il
 est conçu dans le but de surmonter les obstacles actuels entravant l'émancipation des
 femmes, et ce, dans le laps d'une génération.

        Ce scénario même s’il peut paraître optimiste à certains égards repose sur des
 politiques publiques qu’il est possible de mettre en œuvre, pourvu que la volonté soit
 présente. Or, pour favoriser l’adhésion de tous, il faut, d’une part, un effort important
 d’explication et de vulgarisation des programmes envisagés et, d’autre part, un
 accompagnement continu de la population dans ces changements.


                                             76
        En d’autres termes, cela signifie un autre positionnement de l’administration non
plus en tant que simple système de gestion des affaires courantes mais en tant qu’acteur
actif du changement et responsable du changement socio-économique. Sans nul doute,
la compréhension profonde par les citoyen.ne.s des politiques publiques et de leur
intérêt pour eux favoriserait leur adhésion.

    ●   Une famille apaisée

        En 2050, les relations sociales et culturelles femmes-hommes ont tendance à
être perçues comme des relations de coopération et de collaboration pour l’équilibre
de l’institution familiale et de la société entière. Ces nouvelles règles ont été imposées
par les générations Z et Alpha et progressivement ces manières d’être au monde sont
devenues générales, ces jeunes générations ayant massivement utilisé le virtuel pour
dépasser les crispations liées à l’émancipation féminine.

        En particulier, outre le fait qu’elle ait permis d’améliorer les infrastructures du
pays, la coupe du monde 2030 a créé les conditions d’émergence de la population active
féminine forte grâce à la multiplication des chantiers mais surtout au fait que le Maroc
s’est positionné comme vitrine dynamique d’une population accueillante et assoiffée de
vie.

        Cet événement international a en effet eu des retombées favorables sur les
femmes, en stimulant leur autonomisation économique, grâce à la création d'emplois et
à l'essor de l'entrepreneuriat féminin dans les secteurs du tourisme, de la construction
et des services, à la participation sportive des filles, et en mettant en lumière des
modèles féminins inspirants, aptes à favoriser l’évolution des mentalités sans heurts.

        En arrimant l’image du pays déployée sur la scène diplomatique à une jeunesse
moderne, ouverte et avide de vivre mieux, le gouvernement a pu utiliser de manière
significative le capital sympathie acquis au niveau international.

        Ainsi, tout ce qui était auparavant perçu comme des difficultés insurmontables,
notamment les questions de gestion des tâches domestiques au sein des foyers ou
encore de garde des enfants pour permettre à la femme de s’engager dans une carrière
professionnelle, a trouvé des solutions pratiques. En effet, toujours sous l’impulsion de
cette jeunesse, une véritable réflexion sur le sens du travail et de l’existence est menée,
notamment auprès des hommes. À la recherche d’une meilleure qualité de vie, leur
volonté de vivre expressément leur rôle de père, époux ou fils s’est affirmée de manière
forte, ne souhaitant plus sacrifier leurs quotidiens pour des lendemains souhaités
meilleurs. Mieux vivre sa vie s’est rapidement imposé comme un credo généralisé, aussi
bien chez les jeunes hommes que chez les jeunes femmes.

    ●   Un changement de société en toute harmonie

        Ce travail réflexif sur la qualité de vie souhaitée provoque un bouleversement
dans deux dimensions : l’aménagement des conditions de travail et la consistance de
l’État social.




                                            77
       Dans le premier cas, une nouvelle relation de la société avec le travail est définie,
permettant à l’homme comme à la femme de travailler, d’accéder à des postes de
responsabilités mais aussi de participer à l’éducation de leurs enfants, de prodiguer des
soins aux ainés, de mener des actions de citoyenneté et d’animation sociale via la mise
en place d’une panoplie de mécanismes de gestion des conditions de travail (évolution
des modes de contractualisation, flexibilité des horaires, congés parentaux, travail
distanciel, montée en gamme de nouveaux métiers).

        Dans le second cas, l’Etat social complète son dispositif, en plus de la protection
sociale généralisée, par une amélioration qualitative du travail décent, des services
publics, y compris de services de soutien aux catégories défavorisées, et des politiques
économiques d’appui à l’activité et à l’emploi. Là encore, la coupe du monde et sa
conséquence immédiate de redécouverte des liens historiques avec l’Espagne et le
Portugal ainsi que les grands projets structurants menés accélèrent les choix effectués
vers la modernité.

    ●   Un capital humain plus robuste

       En 2050, l’analphabétisme n’est plus qu’un lointain souvenir, la classe
démographique concernée, héritée historiquement, n’existe plus. La transformation
progressive du système éducatif et de formation, certes dans la douleur, favorise une
meilleure adéquation entre l'éducation et l'emploi, en garantissant une formation plus
solide aux individus qui achèvent leur parcours éducatif. Cela les rend plus confiants en
leurs compétences et mieux préparés à évoluer dans le monde professionnel. Il faut dire
que le paradigme éducatif a migré d’un cumul de savoir à posséder, à des compétences
à s’adapter aux situations. Aussi, la possibilité pour chaque individu de révéler ses
compétences et de les renforcer, permet à chacun d'évoluer selon ses souhaits.

      D’un autre côté, cette transformation du système éducatif favorise le
développement personnel des individus à travers leur épanouissement intellectuel,
émotionnel, social et physique, tout en encourageant une citoyenneté active.

    ●   Un système économique en évolution

       Cet affermissement des profils des femmes se manifeste concrètement sur leur
ascension professionnelle qui ne dépend plus exclusivement du marché de l’emploi
national. Leur compétitivité renforcée crée un appel d’air dans l’économie nationale, les
entreprises étant forcées de s’adapter au nouveau contexte. Des politiques ciblées de
promotion de l'investissement et de la diversification économique et d'inclusion des
femmes dans des secteurs porteurs, stimulent la création d'emplois et favorisent une
croissance économique inclusive.

      Aussi, l'évolution du marché du travail permet de préparer une génération
féminine instruite, outillée avec les aptitudes de l’ère de l'exponentialité et la capacité
d’adaptation aux changements futurs.




                                            78
         Enfin, ce vaste mouvement d’intégration organisée de la femme dans la sphère
économique, favorisera son inclusion financière. De nouvelles opportunités d’emploi
sont ouvertes aux femmes à travers une explosion de nouveaux supports de services,
le crowdfunding (138) étant devenu un moyen efficace de mobiliser des fonds, la gig
economy qui offre flexibilité et élimination de certaines barrières traditionnelles à
l'emploi, la « Green Tech » qui permet l'utilisation de l'innovation technologique pour
résoudre des problèmes environnementaux et promouvoir la durabilité en faveur des
femmes. La réhabilitation de la femme dans ses aspirations d’épanouissement social et
économique a développé et renforcé un sentiment de confiance dans les institutions de
l’État, levier essentiel pour booster la consommation endogène.

    ●   Un accès égalitaire aux soins de santé de qualité

        En 2050, le Maroc est parvenu à construire un système de santé équitable et
inclusif qui assure un accès optimal et une qualité supérieure des soins de santé pour
toutes les femmes, indépendamment de leur statut socio-économique ou de leur
localisation géographique.

        Ce système repose sur une approche intégrée qui combine des réformes
structurelles, des investissements ciblés et des initiatives communautaires, pour
répondre aux besoins spécifiques des femmes en matière de santé. Des politiques mises
en place dès la coupe du monde 2030 telles que l'amélioration de la formation et des
conditions de travail des professionnels de la santé, l'investissement dans des
infrastructures publiques modernes spécialisées (santé mentale, gériatrie, ...) et des
solutions d’appoint pour réduire la fracture sanitaire nationale, telles que la
télémédecine ou les caravanes hebdomadaires de santé, qui ont permis de restaurer la
confiance de la population vis-à-vis de ce secteur.

      Egalement, en liaison directe avec l’événement sportif, la promotion d’une
alimentation saine accompagnée de la redécouverte de la diète méditerranéenne, a
permis de rééquilibrer les politiques agricole et industrielle du pays et d’améliorer de
manière substantielle la santé de la population.

    ●   Un futur potentiellement vertueux

       En intégrant les aspirations exprimées lors des consultations avec les expert.e.s,
le futur souhaitable se dessine comme suit.

        En 2050, un Maroc plus inclusif et égalitaire se dessine pour les filles et les
femmes, en conformité avec les engagements internationaux ratifiés. Cette vision
novatrice repose sur des valeurs démocratiques et universelles telles que les droits de
l’Homme, visant à institutionnaliser l'égalité entre les sexes et à consolider l'État de
droit. Elle met en avant l'épanouissement des femmes et des filles tout en préservant
l'identité marocaine, la diversité culturelle, tout en demeurant enracinée dans leurs
traditions.




                                           79
         Cette vision favorise la jouissance des femmes de leur citoyenneté, mettant en
 valeur le patrimoine immatériel du pays. Ce Maroc s’est dirigé progressivement vers
 l’adoption de politiques publiques égalitaires et inclusives, avec une approche centrée
 sur l'égalité femme-homme, avec l’opérationnalisation de l’Autorité pour la Parité et la
 Lutte contre toute forme de Discrimination en tant que mécanisme autonome chargé
 de surveiller les progrès vers l'objectif d'égalité entre hommes et femmes et le Conseil
 Consultatif de la Famille et de l'Enfance en tant que mécanisme chargé de l’élaboration,
 du suivi et de l’évaluation des politiques publiques concernant toutes les formes de
 familles et l’enfance.

        Pour favoriser les transformations sociales, la culture égalitaire a été diffusée
 grâce à une politique éducative et une politique culturelle intégrant ce volet dans toutes
 ses dimensions et composantes. Cet effort a été le prix à payer pour créer le
 changement des perceptions et des comportements de tous. Tout autant que cette
 politique qui constitue un pilier essentiel de l’amélioration de la situation de la femme,
 célébrant la diversité culturelle nationale et favorisant l'intégration de valeurs
 égalitaires dans la société marocaine.

        Cette vision pour le Maroc embrasse également une ouverture dynamique des
 femmes, les positionnant comme des actrices centrales dans la construction de
 partenariats solides à travers le continent africain, et au-delà des frontières atlantiques
 et dans l'arène mondiale. Dans le cadre de cette ouverture, les femmes jouent un rôle
 clé dans ces initiatives, apportant leur expertise et leur leadership pour promouvoir la
 coopération économique, la recherche et l'innovation, ainsi que les échanges culturels.

        Enfin, ce futur souhaitable pour les femmes repose sur une bonne gouvernance
 où la participation des femmes est encouragée et où leur voix est pleinement entendue
 dans les processus décisionnels à tous les niveaux.

4. Préalables et axes de dépassement

       Pour surmonter les obstacles entravent l’évolution des femmes, il est essentiel
 de mettre en place des conditions préalables et des axes de dépassement clairs.

 4.1.   Présentation des préalables

         Le processus d'évolution vers une meilleure condition des femmes au Maroc est
 conditionné par une série de préalables interdépendants qui interagissent de manière
 concomitante dans les dimensions sociales, culturelles, juridiques, économiques et
 politiques. Trois principaux préalables s’avèrent incontournables pour impulser une
 dynamique de changement positif et en accélérer les résultats : mettre en place les
 conditions de développement d’un cadre normatif évolutif, mettre en œuvre des
 politiques publiques convergentes et coordonnées, et systématiser l’anticipation et la
 veille stratégique.




                                             80
    ●   Un cadre normatif évolutif

       Accompagner l’évolution de la société est nécessaire pour répondre à ses
besoins et créer les conditions de son épanouissement. Pour cela, le cadre normatif doit
être en constante évolution pour encadrer au mieux la population. Aussi, dans cette
perspective, il est essentiel de prendre en considération les réalités socioculturelles
propres au contexte marocain, ainsi que les besoins des femmes et des hommes, pour
assurer leur adhésion au changement sans heurts.

        Ce préalable nécessite non seulement un renforcement des capacités des
acteurs du système juridique mais aussi, et surtout, des acteurs producteurs des textes
de lois qu’ils soient issus de l’administration ou du Parlement. L’enseignement du droit
nécessite aussi d’être modernisé pour renforcer la compréhension des acteurs de l’acte
juridique et de la philosophie des lois.

    ●   Des politiques publiques convergentes et coordonnées

        Bien que des progrès aient été réalisés dans l'adoption de politiques publiques
visant à promouvoir l'égalité des sexes et à protéger les femmes contre la discrimination
et la violence, la coordination et la cohérence de ces politiques reste un défi majeur,
indispensable pour assurer leur mise en œuvre effective et leur intégration dans les
pratiques sociales. Sans cette coordination, les politiques publiques ne peuvent être
envisagées que verticalement, donc sans effet multiplicateur sur la politique générale
du gouvernement.

        L’un des problèmes auxquels se confronte toute politique genrée est
l’insuffisance du pouvoir accordé à ses initiateurs et son isolement des autres politiques
publiques menées. Pour dépasser ces contraintes, il est important d’institutionnaliser
les approches genrées dans toutes les politiques publiques, y compris économiques, de
généraliser les plans d’engagement des parties prenantes et de créer des cellules de
suivi aux plus hauts niveaux des institutions.

      Enfin, la mise en place de mesures transversales dans tous les domaines de
développement, ainsi que de programmes spécifiquement ciblés pour répondre aux
besoins particuliers des femmes, est essentielle pour améliorer leur situation d'ici 2050.

    ●   Anticipation et veille stratégique dans les politiques publiques

      L'anticipation et la veille stratégique dans les politiques publiques sont des
processus essentiels pour garantir une action gouvernementale proactive et efficace,
en réponse aux besoins et aux défis spécifiques auxquels les femmes sont confrontées.

       D’abord, ce processus nécessite la collecte de données quotidiennes sur tous les
aspects et domaines de la vie sociale, économique, politique et culturelle tels que
l'éducation, l'emploi, la santé, la violence de genre, en les ventilant par sexe pour
permettre une analyse comparative et identifier les disparités entre les hommes et les
femmes, en vue de saisir les évolutions à long terme et les changements dans les
tendances. Il s'agit ensuite d'identifier les domaines où les femmes rencontrent des
obstacles à leur autonomisation et à leur pleine participation à la société. En utilisant


                                           81
ces informations, le gouvernement peut anticiper les besoins des femmes et concevoir
des politiques publiques adaptées, tout en évaluant régulièrement leur efficacité et en
apportant les ajustements nécessaires pour répondre aux besoins changeants des
femmes.

       Pour améliorer la veille stratégique, il est essentiel de favoriser une approche
participative, incluant les femmes et les hommes dans la conception et l'exécution des
politiques publiques inclusives. Cela nécessite l'établissement d'un partenariat efficace
entre le gouvernement et les différents acteurs, en respectant l'autonomie des
organisations de la société civile et en intégrant la diaspora marocaine. Cette
collaboration permettra le partage des connaissances, des technologies et des
expériences pour favoriser une appropriation des politiques publiques dans un
environnement serein.

4.2.       Présentation des axes de dépassement

       Les axes de dépassement des blocages à la mise en œuvre du scénario raisonné
sont au nombre de quatre : faciliter l’accès des femmes à l’administration via la
généralisation de la gouvernance numérique, renforcer l’accompagnement de la
population dans le changement social par le développement et la valorisation des
métiers sociaux, renforcer l’institutionnalisation de l’accompagnement des femmes
dans l’ouverture au monde et encourager le leadership féminin.

       ●   Généraliser la gouvernance numérique

       Dans le contexte de la transformation numérique du Maroc, la gouvernance
numérique au service des femmes n'est pas simplement une option, mais une nécessité.
Elle permet de dépasser les contraintes de temps et de distance et rapproche les
citoyens des administrations.

       Si le processus de dématérialisation des procédures a été entamé depuis
plusieurs années, il est important de mettre en place une stratégie globale de
transformation numérique inclusive visant à moderniser et à numériser l'administration
publique. Cette stratégie cible le renforcement de la résilience du système tout en
réduisant les écarts numériques, en particulier ceux qui affectent les femmes.

       La gouvernance joue un rôle crucial ans la réussite d'une telle stratégie, en
assurant un pilotage et une coordination efficaces de la transformation numérique.
Cette stratégie prendra en compte les particularités des femmes dans l'accès aux
services publics, tels que l'accès à la justice, aux collectivités locales et aux
administrations publiques, en mettant l'accent sur l'inclusivité et la réduction de la
fracture numérique entre les femmes et les hommes.

        Enfin, cette stratégie exigera des investissements dans le renforcement des
infrastructures numériques à travers le pays, garantissant que toutes les populations, y
compris les femmes des zones rurales et éloignées, aient un accès adéquat à l'Internet
haut débit et aux services numériques.




                                           82
    ●   Renforcer l’accompagnement de la population dans le changement social

       Les métiers d’accompagnement de la population se sont développés ces trois
dernières décennies. Cependant ils ne sont pas suffisamment valorisés et donc ne
permettent pas la fidélisation et la spécialisation des ressources humaines engagées.
Pourtant leur rôle sur le terrain est essentiel à la réussite de tout projet de
développement. Qu’il s’agisse des animateur /ice.s, des accompagnants, des
assistant.e.s sociaux, des ingénieurs sociaux, des médiateur/ice.s, des technicien.ne.s
d’intervention ou autres, ils facilitent la vie de leurs clients dans leurs démarches
quotidiennes et assurent leur adhésion jusqu’à atteinte de leurs objectifs. Au regard de
leur rôle social important dans la réunion des conditions de réussite, des transitions
sociales, dans les projets de développement ou encore dans le rapprochement des
citoyen.ne.s avec les institutions, il semble indispensable de multiplier ces
accompagnants, et ce dans toute initiative de transformation sociale.

    ●   Renforcer l’institutionnalisation de l’accompagnement des femmes dans
        l’ouverture au monde

        Si la relation entre l’individu et le monde est du ressort de l’intime, il est
important que les différents aspects de cette relation soient encadrés et facilités par les
institutions, pour permettre un meilleur bénéfice des initiatives privées.

        Ainsi, qu’il s’agisse de la femme qui va compléter ses études à l’étranger ou de
celle qui va s’y installer un moment de sa vie, le lien avec le pays n’est jamais rompu et
les externalités positives de ces choix méritent d’être valorisées et amplifiées. Un
accompagnement étroit des citoyen.ne.s par les administrations à l’étranger leur
faciliterait le quotidien et renforcerait leur confiance envers leur pays d’origine. De la
même manière, l’accès au monde virtuel et médiatique international gagnerait à être
facilité pour tout ce qui est renforcement des capacités des individus et
conscientisation critique des personnes.

    ●   Promouvoir le leadership féminin

       Le leadership au féminin apporte une série d'avantages intéressants à la fois pour
les entreprises, les administrations et la société dans son ensemble. En effet, en plus de
leurs capacités techniques, les femmes leaders apportent souvent des compétences
supplémentaires, comme par exemple en communication, en intelligence émotionnelle
et en collaboration, lesquelles sont essentielles dans un environnement professionnel
diversifié.

          Certaines actions peuvent favoriser cette promotion du leadership, notamment
(i) l’élimination des biais de genre dans la structure concernée en favorisant leur prise
de conscience via des formations à tout le groupe cible, hommes et femmes, et
l’imposition de règles de parité, (ii) la mise en place des programmes de mentorat et
d’encadrement pour soutenir le développement professionnel des femmes et les aider
à progresser dans leur carrière et (iii) la mise en avant régulière des femmes leaders
actuelles en tant qu’exemples afin d'inspirer les nouvelles générations. Ces figures
doivent évidemment refléter la diversité de la population féminine et du tissu
économique du pays pour faciliter l’identification du public à ces personnes.

                                            83
   Troisième partie

   Proposer. Benchmarking international : un tour d'horizon des
   pratiques prometteuses pour améliorer les conditions des
   femmes

   Chapitre 6. Benchmarking international : des expériences et bonnes
               pratiques prometteuses pour améliorer les conditions des
               femmes
            Le benchmarking permet de mettre en exergue les expériences internationales
   réussies dont le Maroc pourrait s’inspirer pour l'amélioration des conditions des
   femmes. Ce chapitre présente des politiques publiques, des programmes et des
   stratégies, mis en place par divers pays pour relever les défis dans différents domaines,
   susceptibles d’inspirer le Maroc. Les cinq sections suivantes mettront en lumière 13
   exemples de bonnes pratiques provenant de divers pays tels que le Brésil, le Canada, la
   France, la Suède, l'Islande, le Sénégal, la Nouvelle-Zélande, le Singapour, la Colombie,
   l’Italie, le Ghana, la Bolivie et l'Espagne. Ces exemples illustrent des réussites dans
   l'amélioration des conditions des femmes, en lien avec les cinq nœuds leviers identifiés.

1. Promotion d’une culture égalitaire

          La promotion d'une culture égalitaire revêt une importance capitale pour
   promouvoir l'égalité des genres et favoriser l'inclusion sociale des femmes. Cette
   section explore des expériences réussies dans plusieurs pays, notamment au Canada,
   au Brésil et en France. Ces derniers ont adopté des politiques publiques et des lois
   visant à mettre en place des mesures de lutte contre les discriminations basées sur le
   genre et promu des attitudes et des comportements respectueux et équitables. Ces
   mesures législatives s'emploient à démanteler les stéréotypes de genre et à encourager
   une culture égalitaire à travers des politiques gouvernementales et des cadres
   juridiques adaptés.

     ▪   La loi sur le multiculturalisme et le patrimoine culturel au Canada

    La politique officielle du multiculturalisme a été adoptée par le gouvernement canadien le 8 octobre
    1971. Le 1er décembre 1987, la Loi sur le multiculturalisme canadien a été présentée et elle a reçu la
    sanction royale le 21 juillet 1988. Cette loi est considérée comme la première du genre dans le monde.
    Elle permet au Canada de consolider son statut de nation multiculturelle et de présenter le concept de
    multiculturalisme comme un moteur de changements positifs (139).

    La Loi oblige le gouvernement fédéral à s'engager à promouvoir des politiques sur le multiculturalisme
    et maintenir une société diverse et multiculturelle, tel que décrit dans la Politique canadienne du
    multiculturalisme. Elle reconnaît la diversité culturelle et raciale de la société canadienne, favorisant la
    préservation et le partage du patrimoine culturel de tous ses membres. De plus, elle affirme que le
    multiculturalisme est une caractéristique fondamentale de l'identité et du patrimoine canadiens,
    constituant une ressource précieuse pour l'avenir du pays. Elle encourage la participation équitable de
    tous les individus et collectivités à l'évolution de la nation et vise à éliminer les obstacles à cette
    participation.


                                                        84
Elle reconnaît également l'existence des collectivités partageant la même origine et leur contribution à
l'histoire du pays. En outre, elle garantit l'application égale de la loi et la même protection pour tous,
tout en tenant compte des particularités de chacun.

Cette loi a amélioré la condition féminine en reconnaissant et en soutenant les besoins spécifiques des
femmes issues de diverses cultures. Elle a permis de mettre en place des programmes et des initiatives
visant à promouvoir l'égalité des sexes, à combattre la discrimination et à encourager la participation
active des femmes dans tous les aspects de la société canadienne. Ces femmes ont ainsi pu accéder à
de meilleures opportunités éducatives, professionnelles et sociales, contribuant ainsi à leur
autonomisation et à leur épanouissement personnel et collectif.

 ▪   Le Plan National de la Culture au Brésil

Le gouvernement brésilien a mis en place un Plan National de la Culture, approuvé par la loi n° 12.343
du 2 décembre 2010, qui vise à promouvoir et à protéger la diversité culturelle du pays. Ce plan inclut
la création du Fonds National de la Culture, qui est un outil central pour la mise en œuvre de la politique
culturelle gouvernementale. Il repose sur douze principes directeurs, tels que la diversité culturelle, le
droit à la mémoire et aux traditions, la responsabilité socio-environnementale, et la participation
sociale pour la formulation et l'évaluation des politiques culturelles.

Les objectifs majeurs du plan sont l'institutionnalisation d'une politique d'inventaire, de registre et de
sauvegarde des biens culturels immatériels, la contribution à la préservation de la diversité ethnique
et culturelle, la formation d'un réseau de partenaires pour la valorisation et le financement de la
préservation des biens culturels immatériels, et le soutien aux initiatives de préservation développées
par la société brésilienne.

Le gouvernement fédéral joue un rôle crucial dans la normalisation, le financement et la coordination
des programmes de soutien à la culture (140), tandis que la protection du patrimoine culturel est
organisée par le Système National de la Culture, est établie par la loi du Plan de la Culture. Ce système
comprend des organes tant au niveau fédéral qu'au niveau des États-membres, chargés du classement
et de l'enregistrement du patrimoine culturel matériel et immatériel.

Selon la décentralisation administrative du système fédéral, chaque État-membre du Brésil est tenu
d'avoir un organe (IPHAE) chargé du classement et de l'enregistrement du patrimoine culturel régional,
en parallèle de l'Institut national du patrimoine artistique et historique au niveau fédéral (141). Cette
répartition des responsabilités vise à assurer une gestion efficace du patrimoine culturel, à la fois au
niveau national et régional. De plus, l'encadrement juridique de la protection du patrimoine culturel
est divisé entre l'institut du classement historique, qui s'occupe du patrimoine matériel, et l'institut de
l'enregistrement des manifestations culturelles immatérielles (142), qui se concentre sur les aspects
culturels intangibles.

Une évolution majeure de la politique culturelle a été marquée par le Décret n° 3.551 du 4 août 2000,
qui a institué le système national d'enregistrement des biens culturels immatériels. Cet instrument vise
à reconnaître et à valoriser le patrimoine immatériel du Brésil, notamment les savoirs, les célébrations
et les formes d'expression, qui reflètent la diversité culturelle du pays de manière significative
(143)
      .Outre des initiatives spécifiques pour promouvoir l'égalité des sexes dans le domaine culturel,
cette loi a permis de financer des projets et des programmes qui soutiennent les femmes artistes et
créatrices, reconnaissant et valorisant leur contribution au patrimoine culturel et d'encourager leur
participation dans les processus décisionnels culturels, favorisant ainsi leur inclusion et leur visibilité.
Aussi, en soutenant la diversité culturelle, cette loi a contribué à la préservation et à la promotion des
traditions culturelles spécifiques aux femmes, renforçant leur identité et leur rôle dans la société
brésilienne.




                                                    85
     ▪   La loi de lutte contre les contenus discriminatoires sur Internet en France

    La loi n° 2020-766 du 24 juin 2020 constitue une réponse législative aux défis croissants associés à la
    propagation de la haine et toutes les formes de discrimination en ligne. En établissant un cadre
    juridique rigoureux, elle vise à rendre les plateformes numériques responsables de la modération des
    contenus haineux et stéréotypes de genre.

    Elle établit un cadre juridique visant à responsabiliser les plateformes numériques en leur imposant des
    obligations strictes de modération des contenus haineux. Cette loi définit clairement les contenus
    haineux et impose aux plateformes en ligne de mettre en place des mécanismes efficaces de
    signalement et de suppression de ces contenus.

    En imposant des sanctions financières sévères en cas de non-respect de ces obligations, elle vise à
    dissuader les comportements discriminatoires et stéréotypés et à promouvoir un environnement en
    ligne plus sûr et respectueux. Par la création d'une autorité de régulation dédiée, elle renforce la
    surveillance et garantit le respect de ces dispositions, contribuant ainsi à intensifier la lutte contre les
    contenus haineux sur Internet et à promouvoir des normes de conduite en ligne, plus responsables et
    inclusives. Cette loi témoigne de l'engagement de la France à contrer la propagation de la haine en
    ligne et à favoriser un environnement numérique plus sûr et respectueux pour tous les femmes et les
    hommes (144).

    Cette loi a réduit l'exposition des femmes aux violences et discriminations en ligne, qui sont souvent
    sexistes et misogynes. En responsabilisant les plateformes numériques et en imposant des sanctions,
    la loi protège les femmes contre le cyberharcèlement et les discours de haine, contribuant ainsi à leur
    sécurité et leur bien-être numérique. De plus, en combattant les stéréotypes de genre, elle favorise
    une représentation plus équilibrée et respectueuse des femmes dans l'espace public numérique,
    renforçant ainsi leur dignité et leur égalité.


2. Equilibre et harmonie dans l’institution familiale
          La problématique de la gestion de la famille constitue un problème de base
   essentiel à résoudre pour permettre à la femme de s’autonomiser et de prétendre à la
   vie qu’elle souhaite mener. Cela permettrait également aux hommes d’envisager un rôle
   plus actif dans leur cellule familiale, qu’ils soient époux, fils ou pères. La société y
   gagnerait en sérénité mais aussi en engagement. Les exemples choisis proviennent de
   Suède, modèle en la matière, et de Nouvelle Zélande.


     ▪    Politiques familiales inclusives en Suède

    La Suède a mis en place des politiques publiques égalitaires visant à créer un modèle de conciliation
    entre vie familiale et vie professionnelle, centré sur le concept de la "mère moderne » (145).

    En 1969, la théorie de la famille à deux revenus a été introduite comme condition essentielle à l'égalité
    (146)
          , avec l'instauration de l'imposition séparée des couples en 1971. Cette réforme fiscale a incité à
    une répartition égalitaire de l'impôt sur le revenu familial (147).

    L’autre pilier de la politique familiale consiste en un système entièrement intégré sur l’éducation et
    l’accueil de l’enfant, offrant un droit légal à une place pour tous les enfants âgés de 1 an à 7 ans.
     L'État suédois a développé des services de garde d'enfants publics, les services de garde publics
    (förskola ou daghem), les crèches familiales (familjedaghem), les centres pédagogiques ouverts (öppen
    fritidsverksamhet, une allocation de garde (vårdnadsbidrag). Ces services restent donc considérés
    comme un droit de l’enfant.




                                                        86
Pour encourager la participation des pères dans un âge précoce à la vie sociale des enfants (148), la
Suède a instauré le congé parental (Parental Leave Act) (149) en 1974(150), prolongé en 2001) (151), ainsi
que les "dix jours du papa" (152), et les "jours de contact" rémunérés pour les parents d'enfants plus âgés
pour leur permettre de participer aux activités de l’école (enfants handicapés, jusqu’à ses 16 ans).
Le modèle suédois est caractérisé comme d’universaliste et de normatif. Ces réformes ont contribué à
la diminution de la pression sociale pour interrompre sa carrière professionnelle afin de s'occuper de
l'enfant (153).

En Suède, la majorité des couples optent pour le parental (154) et, dans neuf cas sur dix, une partie de
ce droit est exercée par le père (155), avant l’accueil des enfants de 2 ans (88 %) par la förskola (156). Ces
prestations sociales sont financées par le système de protection sociale, (cotisation sociale de 2,97 %
sur les revenus salariaux, à la charge de l’employeur). Elle témoigne de l'engagement de l'État à soutenir
les parents dans la conciliation de leurs responsabilités familiales et professionnelles (157).

Ces mesures ont considérablement amélioré la condition féminine en permettant aux femmes de mieux
équilibrer leurs responsabilités professionnelles et familiales, réduisant ainsi les interruptions de
carrière liées à la maternité. Les congés parentaux et les jours spécifiques pour les pères encouragent
une répartition plus équitable des tâches domestiques et parentales, renforçant la cohésion familiale.
L'accès aux services de garde d'enfants permet aux femmes de retourner plus facilement au travail,
favorisant ainsi leur autonomie économique et leur progression professionnelle.

 ▪   Politiques familiales pour la conciliation travail-famille en Nouvelle-Zélande

La Nouvelle-Zélande s'est fixée pour objectif de devenir l'une des meilleures nations au monde pour
mettre en place des politiques favorisant l’appui aux femmes actives dans le marché de l’emploi.
Plusieurs politiques et programmes dédiés ont été mis en place dans cette optique.

Tout d'abord, en matière d'entrepreneuriat féminin, la Nouvelle-Zélande est arrivée en tête du
classement de l'Indice Mastercard des femmes entrepreneures en 2017 et 2018. Ce palmarès salue
notamment le cadre réglementaire conciliant la vie privée et la vie professionnelle et les conditions
générales très favorables pour encourager les femmes à être des chefs d'entreprise néo-zélandaises.
Le gouvernement soutient activement cet écosystème entrepreneurial féminin via différentes
initiatives :

     ●   Le Ministry for Women propose des programmes de formation et de mentorat dédiés aux
         femmes pour acquérir des compétences entrepreneuriales (Site officiel Ministry for Women).
     ●   Le fonds Wahine Uk O Te Toki accorde des prêts abordables spécifiquement destinés aux
         femmes créatrices d'entreprises (The Conversation).
     ●   La plateforme AllVilleSingapore aide les mères entrepreneures avec les services de garde
         d'enfants intégrés (The Straits Times).

Grâce à ces mesures, les femmes bénéficient d'un meilleur accès aux ressources financières et aux
opportunités entrepreneuriales, ce qui renforce leur autonomie économique. Les congés parentaux
généreux et les services de garde intégrés permettent aux femmes de mieux équilibrer leurs
responsabilités professionnelles et familiales, réduisant ainsi la pression de choisir entre carrière et
famille.

Dans le secteur salarié, la Nouvelle-Zélande promeut aussi l'activité économique des femmes,
notamment à travers des politiques familiales très développées (congés parentaux généreux et services
de garde subventionnés) qui favorisent la conciliation travail-famille (158).

Malgré ces avancées, des défis persistent comme la concentration des femmes entrepreneures dans
certains secteurs traditionnels plutôt que dans les hautes technologies par exemple. Mais grâce à sa
stratégie globale multidimensionnelle, la Nouvelle-Zélande vise à rester un pays de référence pour le
soutien à l'activité économique féminine tout en lui permettant de vivre une vie familiale harmonieuse.




                                                     87
3. Intégration inclusive des femmes au marché de l’emploi

           Les enjeux d'autonomisation économique des femmes et de réduction des
   inégalités professionnelles font aujourd'hui l'objet d'efforts soutenus de la part de
   nombreux pays. Cependant, les approches, les niveaux d'avancées et les leviers d'action
   mobilisés sur ces questions varient considérablement. Qu'ils relèvent des pays
   développés ou émergents, qu'ils privilégient les réformes de lois, les mécanismes
   incitatifs, le soutien à l'entrepreneuriat ou l'accompagnement des femmes salariées, les
   différents cas nationaux témoignent de la diversité des stratégies à l'œuvre.

     ▪   Promotion de l’entrepreneuriat féminin en Colombie

    Pour stimuler l'entrepreneuriat des Colombiennes, le gouvernement a adopté en 2016 une loi
    prévoyant des incitations fiscales pour les entreprises appartenant à des femmes. Celles-ci bénéficient
    désormais d'un crédit d'impôt correspondant jusqu'à 8% des nouveaux investissements réalisés.

    De plus, un programme de microfinance a été renforcé pour faciliter l'accès des femmes au crédit et
    aux services financiers. Cette combinaison de mesures fiscales et financières vise à autonomiser
    économiquement les Colombiennes et à faire progresser leurs activités entrepreneuriales.

    Selon les chiffres de l'Asociación Colombiana de las Micro, Pequeña y Mediana Empresa, seules 24%
    des PME colombiennes appartiennent à des femmes, bien qu'elles représentent 53% de la population
    active. La nouvelle loi de 2016 vise à remédier à ce retard entrepreneurial féminin, notamment en
    milieu rural où il est particulièrement criant. Avec le crédit d'impôt de 8% sur les investissements, le
    gouvernement espère encourager la création de 4 000 nouvelles entreprises par des femmes d'ici 2025
    et de faciliter l'expansion des 800 000 PME existantes dirigées par des Colombiennes (OCDE 2023
    (159)
          ).

    Cette loi a amélioré la condition féminine, en augmentant les opportunités économiques et en
    renforçant la capacité des femmes à créer et à développer leurs entreprises. En offrant des incitations
    fiscales et un meilleur accès aux financements, elle a permis à de nombreuses femmes, de surmonter
    les barrières financières et structurelles. De plus, en ciblant spécifiquement les zones rurales, cette loi
    contribue à réduire les inégalités géographiques et à promouvoir un développement économique plus
    inclusif et équitable.

     ▪   Promotion du travail décent chez les femmes en Islande

    L'Islande est régulièrement citée comme l'un des meilleurs élèves mondiaux en matière d'égalité
    professionnelle entre les femmes et les hommes. Selon les derniers classements du Forum économique
    mondial, elle arrive en tête pour la 12ème année consécutive en 2022 (Global Gender Gap Report
    2022).

    Ce leadership s'appuie sur un cadre législatif parmi les plus stricts et progressistes au monde. Dès 1976,
    une loi interdisait toute discrimination salariale basée sur le genre (Loi n°56/1976). Plus récemment,
    l'Islande a adopté en 2018 une législation pionnière obligeant les entreprises de plus de 25 employés
    à obtenir une certification gouvernementale attestant de leur égalité salariale (Loi n°56/2017 -
    Sources : OIT, BBC).

    Au-delà des salaires, l'Islande promeut des congés parentaux égalitaires exemplaires de 9 mois, dont 5
    mois strictement réservés au père (OCDE). Ce régime extensif participe à une meilleure conciliation
    travail-famille pour les mères (160).

    Ces politiques vertueuses se traduisent par des indicateurs au sommet mondial. Avec 85,1% en 2021,
    l'Islande affiche l'un des taux d'emploi féminin les plus élevés d'Europe (Eurostat). L'écart salarial n'est
    plus que de 11,3%, contre 15% en moyenne dans l'UE (Eurostat 2020).



                                                        88
    Des défis subsistent néanmoins, telle une ségrégation professionnelle persistante qui concentre les
    femmes dans les secteurs éducation et santé. Mais par ses lois pionnières, congés parentaux avant-
    gardistes et résultats tangibles, l'Islande montre la voie vers plus de travail décent pour les femmes.

    Ces politiques ont non seulement renforcé l'autonomie économique des femmes en leur assurant des
    revenus équitables, mais elles ont aussi favorisé une plus grande participation des hommes dans les
    responsabilités parentales. En mettant en avant ces initiatives, l'Islande illustre comment des lois
    progressistes peuvent créer un environnement professionnel plus inclusif et égalitaire, bénéficiant à
    l'ensemble de la société.

     ▪   Promotion de l’entrepreneuriat féminin à Singapour

    Singapour s'est récemment affirmée comme champion de la promotion de l'entrepreneuriat féminin au
    travers d'initiatives gouvernementales et privées ambitieuses, en particulier dans les domaines d'avenir
    comme les cleantechs.

    En 2022, l'accélérateur privé Accelerating Asia (161) a lancé un programme dédié "The Women in
    ClimaTech and Sustainability Reverse Accelerator" visant à former et financer 30 start-ups deep tech
    dirigées par des femmes dans les secteurs des technologies climatiques et du développement durable.
    Ce programme intensif de 4 mois combine mentorat d'expertes, formations techniques et
    commerciales, et un financement en capital-risque allant jusqu'à 300 000 dollars singapouriens par
    start-up sélectionnée. L'objectif affiché est d'accélérer la croissance de ces entreprises à fort impact
    positif sur le climat, tout en faisant émerger une nouvelle génération de femmes entrepreneures de
    pointe.

    Cette initiative s'inscrit dans la stratégie plus large de Singapour pour devenir un hub régional de
    l'innovation féminine.

    Si des défis socio-culturels persistent, Singapour déploie donc des moyens ambitieux, du financement
    aux services d'accompagnement en passant par des mécanismes incitatifs, pour se positionner comme
    une plaque tournante régionale de l'entrepreneuriat féminin de pointe dans des secteurs d'avenir. Ces
    initiatives ont contribué à promouvoir l'autonomisation économique des femmes dans des secteurs
    clés de l'économie durable.


4. Amélioration de l’accès égalitaire aux soins de santé

           Le benchmark de l’amélioration de l'accès égalitaire aux soins de santé
   présentera des initiatives réussies pour l’élargissement de la protection sociale avec des
   allocations et des prestations favorables aux femmes. Les expériences sont relatives à
   quatre pays, notamment le Ghana, la Bolivie, la Suède et l’Italie.




                                                      89
 ▪   Extension de l’assurance maladie communautaire au secteur informel au Ghana

Le Ghana a mis en place des régimes d'assurance maladie communautaire créés par des associations
communautaires, des coopératives ou des fournisseurs de soins de santé. Ces derniers permettent aux
travailleurs du secteur informel, dont la majorité sont des femmes employées dans l’économie
informelle, d'accéder aux services de santé sans frais au moment de la prestation. Pour élargir la
couverture et réduire les coûts administratifs, l'Institut de Sécurité Sociale et d’Assurance Nationale a
mis en place un système à trois piliers : un régime de sécurité sociale de base contributif, un mécanisme
privé obligatoire pour des prestations forfaitaires, et des régimes de pensions individuels. Par
conséquent, le Fonds de sécurité et d’assurance national (Security and National Insurance Trust)
(SNNIT) a mis en place en février 2008 le Fonds pour le secteur informel (Informal SectorFund) sur la
base du succès d’un projet pilote démarré en mai 2005. En février 2008, le Fonds pour le secteur
informel (SIS), a créé un régime de retraite contributif volontaire sans cotisation préétablie, qui a été
lancé sur la base d'un projet pilote de 2005. Les versements sont crédités à parts égales dans les deux
sous-comptes de l’épargnant : (i) le compte affecté au régime professionnel et (ii) le compte de retraite.

Le SIS, en partenariat avec la banque HFC et une institution de microfinance, propose des options
d'épargne retraite et des services financiers adaptés aux travailleurs informels. En 2011, il comptait
déjà 90 000 membres avec des objectifs ambitieux pour les années suivantes. Ce régime volontaire
spécial pour les travailleurs du secteur informel répartit les cotisations à parts égales entre une caisse
de pensions et un fond de prévoyance ce qui permet d’utiliser partiellement les cotisations
individuelles pour financer les frais de scolarité et l’assurance maladie ou pour faire face à une
mauvaise conjoncture économique (162).

Par ailleurs, le Programme « Livelihood Empowerment Against Poverty » (LEAP) fournit aux personnes
pauvres de plus de 65 ans une allocation mensuelle de 8,15 USD (163). L'expansion des régimes de
retraite au secteur informel repose sur la flexibilité des contributions, le ciblage des épargnants
potentiels et des incitations, utilisant une large gamme de prestataires de services. Cette initiative
montre qu'il n'existe pas de modèle unique de sécurité sociale et de retraite, le Ghana a développé des
mécanismes adaptés à son contexte social, culturel et économique. Dans lesquels, les partenaires
sociaux jouent un rôle crucial dans la mise en place de régimes complémentaires, tandis que l'État a
prévu un cadre réglementaire et des mécanismes de supervision efficaces, ciblant particulièrement les
personnes à revenus faibles ou moyens pour éviter les injustices et le déséquilibre social (164).

L’AMC contribue à empêcher que davantage de familles ne tombent dans la pauvreté à cause des
paiements directs des soins de santé. Elle contribue aussi à mieux sensibiliser les gens à l’importance
des mécanismes de protection sociale de la santé financièrement abordables et viables. Cette
approche suscite donc un intérêt croissant, mais elle n’en comporte pas moins certaines insuffisances
comme les faibles taux de couverture, la grande variété des programmes, les différences dans la
transférabilité des droits, les graves contraintes administratives et financières, ...

 ▪   Mise en place d’une pension universelle : Pension de solidarité en Bolivie

Depuis le 1er février 2008, le gouvernement bolivien a instauré la "Rente vieillesse universelle
Dignité", une allocation non contributive destinée aux personnes de 60 ans et plus sans autre source
de revenu. Cette rente équivaut à deux cinquièmes du salaire minimum, financée par les recettes
pétrolières, principalement dans la caisse de l’Impôt direct sur les hydrocarbures (IDH). Cette rente est
également financée par les dividendes provenant des entreprises publiques opérant dans les secteurs
stratégiques. D’ailleurs, la gestion des ressources et du système de paiements en ligne ainsi que le
contrôle des transactions sont assurées par un organisme indépendant.

Pour les bénéficiaires ne recevant aucune autre pension, le montant annuel des prestations est de 2
400 bolivianos (environ 340 dollars). Ceux qui perçoivent déjà une retraite reçoivent 75 % de ce
montant, soit 1 800 bolivianos (environ 255 dollars). Cette distinction vise à accorder une priorité,
avec un paiement plus élevé, aux personnes, particulièrement les femmes, sans pension de vieillesse,
tout en garantissant le droit universel à une pension (165).




                                                   90
    En Bolivie, le financement de la pension de solidarité peut se faire par l’impôt à travers deux formes. Il
    peut s’agir d’une pension universelle uniforme sans condition de ressources, tous les résidents ou
    citoyens du pays ayant atteint l’âge de la retraite pouvant en bénéficier ou bien il peut s’agir d’une
    pension sous conditions de ressources, différentielle, complétant les revenus du retraité de telle sorte
    qu’ils atteignent un certain seuil. Même en fournissant un montant faible, la Rente Dignité constitue
    l’un des trois piliers de la lutte contre la pauvreté monétaire engagée par le Gouvernement. D’ailleurs,
    plus de trois Boliviens sur cinq vivent avec moins de 2 dollars par jour, 37% ne disposant même que
    de moins de 1 dollar (166).

   ▪    Avantages pour les femmes dans le système de protection sociale en Suède et en Italie

        La Suède accorde des avantages aux femmes, il serait intéressant d’en citer quelques-uns ci-
        dessous :

        •   Les droits à la pension attribués pour les années consacrées à l’éducation des
            enfants ;

        •   Le plafond fixé pour les prestations mais pas pour les revenus en faveur des
            travailleurs à faibles revenus et, par conséquent, des femmes ;

        •   Les tables de mortalité unisexes (ne font pas la différence entre les sexes),
            redistribuent le revenu en faveur des femmes ;

        •   La pension garantie, indexée sur le montant de la retraite, redistribue les revenus en
            faveur des travailleurs à bas salaires et, par conséquent, des femmes.

    En 1990, le transfert de la pension au conjoint survivant sans distinction de genre était adopté à la
    place de la pension de veuvage (167).
        L’Italie a la particularité de prendre en compte certaines périodes pour le calcul de la pension
        notamment les périodes de chômage, de formation professionnelle, les années consacrées à élever
        des enfants de moins de 6 ans, les périodes d’absence relative à la maladie d’enfants de plus de 7
        ans (168).


5. Intégration de la femme dans le système de gouvernance

          Le benchmark relatif à la place de la femme dans les systèmes de gouvernance
   met en exergue l’importance de l’existence d’un cadre normatif global favorisant la mise
   en œuvre de la parité. Un tel cadre a permis des avancées réelles en renforçant de
   manière significative la participation des femmes aux systèmes de gouvernance et leur
   contribution à la décision, constituant ainsi une évolution forte vers l’égalité de genre
   en tant que droit fondamental.
    ▪   Loi organique pour l’égalité effective et loi pour la parité en politique et dans les entreprises en
        Espagne

    La loi organique pour l'égalité effective des femmes et des hommes (es), adoptée par les Cortes
    Générales d'Espagne en mars 2007, vise à lutter contre les inégalités de genre, notamment dans les
    domaines de l'emploi, de la représentation politique et de la lutte contre les discriminations. Elle impose
    aux partis une part de 60 % au maximum et 40 % au minimum de candidats de chaque sexe sur les
    listes et ce, par tranche de cinq candidats. Concrètement, il est apparu que les partis avaient positionné
    les femmes de manière moins avantageuse, celles-ci ouvrant et clôturant fréquemment chaque tranche
    de cinq candidats sur les listes, tandis que les hommes occupaient les positions centrales.



                                                        91
Deux conclusions peuvent être tirées de ce demi-échec : d’une part, le procédé par tranche s’est révélé
défavorable aux femmes, dès lors qu’en règle générale, on ne comptait pas plus de deux femmes pour
cinq candidats, parfois moins. D’autre part, un tel résultat indique qu’en dépit des progrès indéniables
que constituent un gouvernement paritaire et un ratio de 40/60, davantage reste à faire pour remettre
en cause les traits patriarcaux des cultures politiques, tels qu’ils sont inscrits dans les structures
institutionnelles.

C’est pourquoi le Conseil des ministres espagnol a approuvé mardi 7 mars 2023 un avant-projet de loi
visant à instaurer la parité en politique et dans les entreprises. Ce texte, qui vient d'être adopté en juin
2024 par le Parlement, vient transposer une directive européenne mais va plus loin que les objectifs
définis au niveau de l’UE. “les instances de représentation des métiers, conseils, ordres, collèges ou barreaux,
devront eux aussi respecter la parité de 40 %, de même que les jurys décernant des prix financés en partie
par les administrations publiques”. Et dans le monde politique, “les partis auront l’obligation de présenter
des listes alternant un homme et une femme à toutes les élections : municipales, régionales, législatives et
européennes”. Enfin, la parité devra aussi être respectée dans le gouvernement, un pas de plus vers la
parité. « Si les femmes représentent la moitié de la société, alors la moitié du pouvoir politique et économique
doit être aux mains des femmes. ». Le projet de loi instaure l’obligation d’une représentation paritaire
aussi bien dans la sphère politique que dans la direction des entreprises. Cette évolution législative
témoigne de l'engagement continu de l'Espagne à promouvoir l'égalité de genre et à renforcer la
présence des femmes dans les instances de décision, contribuant ainsi à améliorer leur condition et à
favoriser une société plus inclusive et équitable.


▪   La loi sur la parité en France

La loi constitutionnelle n°99-569 du 8 juillet 1999, ajoute à la Constitution un amendement affirmant
que « La loi favorise l'égal accès des femmes et des hommes aux mandats électoraux et fonctions
électives ». La loi ordinaire n° 2000-493 du 6 juin 2000 met en application la loi constitutionnelle de
1999, par diverses mesures. Elle tend à favoriser l'égal accès des femmes et des hommes aux mandats
électoraux et fonctions électives. Cette loi dite sur « la parité » contraint les partis politiques à présenter
un nombre égal d’hommes et de femmes pour les élections municipales, régionales, sénatoriales et
européennes. Elle a ainsi joué un rôle crucial dans l'amélioration de la condition des femmes en
politique. Cette disposition est coercitive puisque les listes qui ne respectent pas la parité ne sont pas
enregistrées. Pour les élections législatives, le système n’est qu’incitatif. Les partis qui ne présentent
pas 50 % de candidates se voient appliquer une retenue financière.

La loi de 2000 est lacunaire puisqu’elle ne concerne ni les élections municipales dans les villes de moins
de 3 500 habitants, ni les cantonales, ni les sénatoriales dans les départements qui élisent moins de
trois sénateurs. Pour corriger certaines faiblesses de cette loi, la loi n° 2007-128 est promulguée le 31
janvier 2007. Celle-ci entend d’abord féminiser les exécutifs locaux (communes de plus de 3 500
habitants, régions) en prévoyant l’application de la parité pour l’élection des adjoints au maire ainsi que
pour les membres de la commission permanente et les vice-présidences des conseils régionaux. Les
élections cantonales entrent dans le champ du dispositif paritaire. Désormais, les candidats doivent
avoir un suppléant de sexe différent. Cette loi a permis d'accroître la visibilité et la participation des
femmes aux échelons locaux et régionaux, là où elles étaient historiquement sous-représentées.
Désormais, les candidats doivent avoir un suppléant de sexe différent. Ces dispositifs contraignants,
comme l'obligation de constituer des binômes paritaires pour les élections départementales et
municipales dans les grandes communes, ont contribué à une meilleure intégration des femmes dans
la gouvernance locale.

La loi organique du 17 mai 2013 relative à l'élection des conseillers départementaux, des conseillers
municipaux et des conseillers communautaires modifie de façon substantielle les scrutins locaux. Les
conseillers départementaux qui se substituent aux conseillers généraux sont désormais élus au scrutin
binominal à deux tours. Les binômes sont obligatoirement composés d'un homme et d'une femme.
Pour le scrutin municipal, l'obligation de parité pour la composition des listes s'applique désormais dans
les communes de 1 000 habitants et plus.




                                                      92
La loi du 27 décembre 2019 relative à l'engagement dans la vie locale et à la proximité de l'action
publique prévoit la modification du Code électoral afin de renforcer la parité au sein des exécutifs des
établissements publics de coopération intercommunale (EPCI). La loi révise le pacte de gouvernance
entre les EPCI et les communes membres afin de fixer des objectifs de parité aux instances de
gouvernance et aux commissions. Le renforcement de la parité dans les intercommunalités et les
communes est repoussé à un futur texte dont les dispositions s'appliqueront en 2026.

La législation en faveur de la parité a donné des résultats contrastés selon les modes de scrutin. Le
scrutin de liste, assorti de contraintes strictes quant à la composition paritaire des listes de candidats,
a permis à la parité de devenir une réalité effective dans les conseils municipaux des communes de
plus de 1 000 habitants, dans les conseils régionaux, dans les conseils départementaux et dans la
représentation française au Parlement européen. Les élections européennes sont régulièrement citées
comme exemplaires en matière de parité : 39 femmes et 40 hommes ont été élus en mai 2019 sur les
79 eurodéputés français.

La part des femmes dans les conseils municipaux augmente et atteint 42,4% après les élections en
2020 selon la Direction générale des collectivités locales (DGCL). La part des femmes dans les conseils
communautaires augmente et atteint 35,8 % après les élections en 2020. Les femmes représentent
48% des conseillers régionaux et territoriaux, et 50,3% des conseillers départementaux, toujours selon
la DGCL. En revanche, dans les communes de moins de 1 000 habitants, la loi n’étant pas
contraignante, les avancées de la parité sont plus limitées : 37,6% de femmes dans les conseils
municipaux après les élections de 2020 contre 46,6% dans les communes de 1 000 habitants et plus.
Si les lois sur la parité ont permis d'améliorer la place des femmes en politique, celles-ci restent encore
exclues des fonctions à haute responsabilité. Malgré la promulgation de la loi de 2007 qui impose la
parité dans l’élection des adjoints, la proportion de femmes élues maires reste faible (19,8% après les
élections de 2020). La loi a bien fonctionné également pour les élections régionales. De 1995 à 2004,
le pourcentage de conseillères régionales passe de 27,5% à 47,6%. En 2010, après l’entrée en vigueur
de la loi de 2007 qui impose la parité au sein du conseil régional, dans la commission permanente et
dans les vice-présidences, la présence des femmes dans les exécutifs régionaux progresse fortement.
Les femmes occupent 48,1% des mandats exécutifs. Cependant, la loi ne posant pas d’obligation pour
les têtes de listes, seules quatre femmes sont présidentes de régions.

Par contre, la parité n’a que très peu progressé pour les élections qui reposent sur un scrutin
uninominal. C’est notamment le cas pour les élections législatives. Si la proportion de femmes
candidates au premier tour a augmenté, la proportion de femmes élues à l’Assemblée nationale est
passée de 10,9% en 1997, à 12,3% en 2002, puis 18,5% en 2007 et 26% en 2012. Les élections
législatives de juin 2017 ont vu le nombre de femmes élues battre un record avec 224 députés femmes,
soit 38,8% des 577 sièges de députés. Mais, le scrutin de juin 2022 a vu le nombre de femmes reculer,
avec 217 femmes élues. Si l'Assemblée nationale se féminise, il reste encore des partis politiques qui
préfèrent payer des pénalités plutôt que d’investir des femmes à la place des députés sortants (169).
Ainsi, la législation sur la parité en France a joué un rôle significatif dans la promotion de l'égalité
politique entre hommes et femmes, contribuant ainsi à renforcer la démocratie et à améliorer la
condition féminine dans la sphère publique.

▪   Loi sur la parité absolue au Sénégal

 La loi n° 2010-11 du 28 mai 2010 sur la parité « absolue » stipule que 50 % de femmes doivent figurer
sur les listes de tous les scrutins, avec un système précis alternant hommes et femmes pour éviter que
ne soient inscrits 10 hommes en premier, et les femmes ensuite. L’innovation majeure de la loi
sénégalaise sur la parité est son caractère contraignant. Les articles 1 et 2 de la Loi n°2010-11 du 28
mai 2010 sur la parité absolue stipulent que « les listes de candidatures doivent être alternativement
composées de personnes des deux sexes, et que lorsque le nombre de membres est impair, la parité
s’applique au nombre pair immédiatement inférieur. Les listes de candidatures doivent être conformes
à cette disposition sous peine d’irrecevabilité ». Le décret N°2011-819 du 19 mai 2011 précise son
application dans les listes de candidature. Le Code électoral sénégalais, en son article LO.145, abonde
dans le même sens de contraindre les partis politiques et coalitions de partis politiques à l’application
scrupuleuse de la loi sur la parité absolue Homme-Femme.


                                                    93
 Cette loi a été expérimentée pour la première fois lors des élections à la députation du 1er juillet 2012
 au cours de laquelle il est constaté une forte représentation des femmes. De 22% (soit 33 députés)
 pour la législature 2007-2012, l’effectif des femmes députées est passé à 43,3% (soit 64 députés) pour
 la législature 2012-2017, et à plus de 44% en 2022.

 Cette expérience n’a pas été tout à fait aisée au début pour bon nombre de listes de candidatures.
 Celles-ci, sous risque d’être déclarées irrecevables, étaient obligées de se passer de certains de leurs
 barons (généralement des hommes) pour se conformer à la loi, et d’autres, faute de responsables
 féminins charismatiques, peinent à trouver des candidates. De plus, en intégrant davantage les femmes
 dans les sphères décisionnelles, cette loi a contribué à promouvoir l'égalité des genres et à remettre en
 question les normes socio-culturelles préexistantes, qui limitaient la participation des femmes à la
 politique. Ainsi, la loi sur la parité absolue au Sénégal a non seulement renforcé la démocratie en
 favorisant une représentation plus inclusive, mais elle a également été un levier essentiel pour
 l'amélioration de la condition féminine, en promouvant l'égalité des chances et la diversité dans la
 gouvernance politique du pays.



Chapitre 7. Les orientations des politiques publiques, des nouvelles voies
            pour construire un avenir meilleur pour les femmes en 2050

      L’une des caractéristiques des sociétés en développement est qu’elles évoluent
à des vitesses différenciées selon les acteurs en présence, la cohésion sociale des
groupes existants et leurs conditions de vie actuelles et potentielles.

       Les politiques publiques doivent dans ce contexte orchestrer ces évolutions
pour, d’une part, créer les conditions d’un cycle vertueux positif et, d’autre part, réduire
les inégalités sociales qui pourraient remettre en cause la dynamique. Ainsi, le Maroc,
pays en transition multiple, se doit de relever le défi de faire évoluer son modèle social
et économique vers un modèle qui soit en phase avec les exigences du paradigme d’un
développement humain durable et ce, en assurant les conditions nécessaires pour
réussir à la fois l’intégration de l’économie nationale dans la nouvelle division
internationale du travail et l’atteinte d’un bien-être social pour tous.

       Afin de défaire les nœuds qui entravent une meilleure participation de la femme,
des orientations de politiques publiques sont proposées, s’appuyant sur les initiatives
menées jusqu’à présent afin de les renforcer et explorant les pistes encore peu
investies.

        Celles-ci sont présentées selon les nœuds : les normes sociales discriminantes,
les mutations de la famille qui engendrent des rapports déséquilibrés, le marché de
l’emploi tendu et non inclusif, l’accès inégalitaire aux soins de santé de qualité et le
déficit du système de gouvernance entravant la participation entière des femmes.

       Ceux-ci trouveraient des issues favorables à travers la prise en considération des
attentes de la population, dont les femmes en premier lieu. Il n’est pas, en effet, à
négliger que l’évolution de la société a largement dépassé les limites fixées par la norme
juridique actuelle, chacun et chacune agissant selon ses propres intérêts. De ce point
de vue, le cadre réglementaire doit rattraper son retard et plus encore, dépasser les
attentes de la population afin de créer des conditions de vie sociale justes et équilibrées
valables aussi pour les générations à venir.

                                                    94
           Dès lors, il est crucial d'adopter une approche réfléchie et consolidée qui intègre
   à la fois la modernité, les références religieuses, les normes juridiques et les impératifs
   de santé publique. Cela permettra de concevoir des politiques publiques alignées sur
   les attentes sociales, culturelles, sociétales et religieuses, tout en contribuant à la
   construction d'un État moderne.

1. Investir dans une transformation culturelle et éducationnelle inclusive et porteuse
   d'égalité
           Afin de dépasser les normes sociales discriminantes qui persistent, il est
   nécessaire de renforcer les initiatives actuelles avec plus de détermination, les
   généraliser et approfondir certains aspects encore peu défrichés pour donner une
   chance à la transformation des perceptions et des comportements d’avoir lieu.
   Les orientations des politiques publiques sont organisées selon deux axes :
   l’investissement dans la culture de l’égalité et l’investissement dans l’éducation
   transformationnelle.

❖ Ancrer la culture de l’égalité en tant que vecteur d’une transformation sociétale

  •   Promouvoir l'égalité dans les médias audiovisuels : institutionnaliser des régulations
      strictes pour éliminer les stéréotypes de genre dans la production, la sélection et la
      diffusion des programmes télévisés.

  •   Renforcer en continu les cadres de l’administration pour combattre les inégalités de
      genre : mise en œuvre de changements pratiques au sein des administrations, pour
      en faire des modèles d’égalité et d’inclusion sociale.

  •   Créer une nouvelle catégorie professionnelle pour le changement social :
      accompagnement des populations cibles et correction des pratiques discriminatoires
      à l’égard des femmes dans les politiques publiques.

  •   Promouvoir des expressions artistiques des femmes marocaines dans le capital
      culturel marocain : valorisation du riche patrimoine culturel du Maroc pour
      promouvoir une culture égalitaire et non stéréotypée.

  •   Encourager le rayonnement international de la place de la femme dans la culture
      marocaine : mise en valeur de la culture marocaine comme une contribution
      significative à l’humanité, en mettant en avant les modèles de femmes porteurs des
      valeurs de générosité, de partage et de dialogue.

  •   Elaborer une politique numérique inclusive visant à encourager l'innovation tout en
      respectant une utilisation éthique de la technologie, pour lutter contre la
      discrimination algorithmique, les inégalités digitales, le Trolling, le doxing et le
      hacking, dans le but de protéger les femmes contre toutes formes d'abus
      d'exploitation en ligne.




                                               95
❖ Promouvoir l'éducation transformationnelle,              comme      stratégie    clé   pour
  l'autonomisation des femmes

  •   Moderniser l’offre éducative au prisme de l'égalité et de l'inclusion : rénover en
      continu la formation de l'école publique en harmonie avec les besoins des filles et
      des femmes du XXIe siècle et la révolution numérique, en intégrant de nouvelles
      compétences sociales et culturelles essentielles comme la pensée critique et
      l’adaptabilité et la citoyenneté.

  •   Renforcer le programme de développement intégré de la petite enfance : rénover les
      programmes visant à soutenir le développement des petites filles et garçons au
      niveau des compétences, physique, cognitif, social et psychique, constitue le socle
      d’investissement dans le capital humain.

  •   Investir dans des programmes de renforcement du lien social à l’école : pousser la
      génération future dans l’engagement civique et le volontariat, les conscientiser dès
      le jeune âge à leur rôle dans la responsabilité individuelle et collective du respect des
      droits des femmes.

  •   Impliquer de manière accrue les parents (mère et père) dans la politique éducative :
      accorder une place renforcée aux parents dans les décisions éducatives, pour
      renforcer la collaboration entre l'école et les familles.

  •   Promouvoir la démocratie participative par la société civile en faveur des droits des
      femmes : soutenir l'utilisation des droits constitutionnels par la société civile, à
      travers la vulgarisation d'outils permettant l'expression des volontés collectives
      (pétitions, motions, consultations publiques) pour promouvoir les droits des femmes.

  •   Soutenir la recherche scientifique sur les droits des femmes : investir de manière
      significative dans la recherche scientifique pour produire des données à caractères
      socio-économiques permettant de suivre et d'analyser les transformations de la
      société marocaine, contribuant ainsi à l'amélioration des conditions des femmes.

2. Une stratégie de politique familiale cohérente et renforcée
           La famille n’a jusqu’à présent jamais fait l’objet d’une politique dédiée. Cette
   entité a toujours été considérée comme naturelle, évidente et allant de soi. A la base de
   l’organisation sociale, ses dysfonctionnements sont de véritables freins au
   développement du pays. Pourtant, force est de constater que la famille est autant
   malmenée, sinon plus que les autres structures d’organisation socio-économique, lors
   des périodes de crises économiques et de mutations sociales d’envergure. Les femmes
   dans ces situations payent la facture la plus lourde, étant généralement en charge des
   soins aux autres. Les orientations proposées sont au nombre de trois : consolider la
   cellule familiale, permettre à la femme de conjuguer vie professionnelle et vie familiale,
   et investir dans le bien-être et la santé des femmes.




                                               96
❖ Renforcer la cellule familiale pour promouvoir l'épanouissement des femmes

  •   Promouvoir l'équilibre travail-vie personnelle pour renforcer les liens familiaux, en
      réduisant le temps de travail pour les hommes et les femmes, favorisant ainsi un
      engagement accru dans la vie familiale.

  •   Elargir et généraliser le congé de paternité dans le secteur privé, renforçant ainsi le
      rôle parental des hommes dès les premiers stades de la vie de famille leur permettant
      de soutenir leur épouse durant le congé de maternité.

  •   Mettre en place des politiques de travail flexibles qui permettent aux travailleurs,
      hommes et femmes, de consacrer du temps à leurs familles sans préjudice pour leur
      carrière ou leur sécurité financière à long terme.

  •   Elaborer une politique de vieillesse inclusive intégrant des mesures spécifiques pour
      la prise en charge adéquate des femmes âgées, reconnaissant les défis spécifiques
      auxquels elles sont confrontées en matière de santé, de sécurité économique et de
      bien-être social.

  •   Créer des espaces de loisirs familiaux de proximité, renforçant les liens
      intergénérationnels et contribuant au bien-être global des familles marocaines.

❖ Mettre en œuvre des stratégies pour favoriser l'équilibre entre vie professionnelle et
  vie familiale des femmes

  •   Développer des structures de prise en charge des enfants au sein de l’école mais
      aussi dans les entreprises et les administrations, pour permettre à la mère et au père
      de se consacrer à leurs carrières.

  •   Professionnaliser les métiers du care et la garde des enfants, en envisageant les
      gardiennes à domicile ou les garderies en horaires décalés, pour répondre aux
      besoins spécifiques des femmes ayant des horaires atypiques ou des besoins de
      garde particuliers.

  •   Octroyer une aide financière aux parents qui inscrivent leurs enfants dans des
      structures organisées de garde.

  •   Promouvoir de nouveaux modes de travail flexibles (horaires décalés, travail à
      distance ou en hybride) aussi bien pour l’homme que pour la femme.

  •   Développer une politique de valorisation des carrières des femmes, pour leur éviter
      d’être pénalisées en termes d’accès à des postes de responsabilité, du fait de leur
      maternité.

  •   Investir dans la robotique ménagère de qualité et la domotique pour faciliter la prise
      en charge et le partage de tâches ménagères quotidiennes effectuées par les femmes
      et les hommes.




                                              97
3. Concevoir des politiques de l’emploi socialisées permettant une intégration
   professionnelle entière, égalitaire et épanouissante

          Une transformation de paradigme du développement économique est
  nécessaire, préconisant que l'action publique en matière d'emploi soit menée selon une
  approche similaire à celle des politiques de la santé, de l'éducation et de
  l'environnement, dans une logique d'économie publique.

         Cette nouvelle perspective de la politique publique de l'emploi, découlant de
  cette approche d'économie publique, place l'emploi au cœur du développement
  économique, l'emploi étant considéré non pas comme une variable résultante, mais
  comme une variable centrale et objective. L'objectif est triple : élargir l'offre d'emplois
  pour inclure les chômeurs, consolider les emplois existants et favoriser l'évolution des
  emplois à faible productivité vers des emplois plus productifs.

          Quatre leviers principaux peuvent être actionnés pour la mise en œuvre de cette
  nouvelle vision de l’emploi : la croissance, la qualité, la connectivité et la
  territorialisation.

  •   La croissance implique des mesures visant à stimuler la création d'emplois, tant dans
      une optique commerciale que dans une optique sociale ou de service public.

  •   La qualité (productivité, revenu et sécurité) se concentre sur l'accompagnement
      visant à améliorer la qualité des emplois existants, en favorisant la transition des
      emplois précaires et peu productifs (travail indépendant et emploi salarié) vers des
      emplois décents et productifs.

  •   La connectivité comprend des mesures visant à encourager une participation
      équitable des femmes en âge de travailler au marché du travail, en éliminant les
      obstacles qui pourraient les empêcher d'entrer sur le marché du travail ou de trouver
      un emploi.

  •   La question de l'emploi est étroitement liée aux territoires, ce qui nécessite de
      prendre en considération les spécificités et les besoins propres à chaque région, lors
      de la conception et de la mise en œuvre des politiques d'emploi. Cela implique de
      développer un mode d’intervention différent du schéma traditionnel d’un État
      centralisateur et bureaucratique et de reconnaître que les dynamiques
      économiques, sociales et culturelles peuvent varier d'une région à l'autre, et donc
      d'adapter les stratégies d'emploi en conséquence. Trois axes d’intervention se
      distinguent : les nouveaux paradigmes permettant la prospérité économique des
      femmes, les opportunités d’emploi pour les femmes et l’amélioration du cadre
      juridique et réglementaire du travail.




                                              98
❖ Orientations stratégiques vers de nouveaux paradigmes permettant la prospérité
  économique des femmes

  •   Renforcer les capacités de Gouvernance du Marché du Travail en faveur des
      femmes : élaborer un plan pour le renforcement des capacités de l’État, échelonné
      sur différents horizons temporels et territoriaux, et l’ériger comme priorité absolue
      des pouvoirs publics, et ce, pour renforcer les compétences du Maroc en expertise
      et en outils de pilotage, nécessaires à l'appropriation réussie de la transformation du
      modèle économique de développement et au suivi des politiques publiques de
      l’emploi. Cela implique de mobiliser les ressources internes du pays et de solliciter le
      soutien de la coopération internationale.

  •   Elaborer une politique d’industrialisation à échelle humaine pour favoriser à la fois la
      diversification de l’économie à travers l’accroissement de sa complexité, et le
      développement d’un tissu étoffé de PME-PMI compétitives qui peut répondre aux
      besoins d’approvisionnement croissants des chaînes de valeur mondiales. Cette
      politique inclura en octroyant des incitations fiscales, des subventions et un
      accompagnement pour encourager la création et le développement d'entreprises
      dirigées par des femmes.

  •   Développer une politique, axée sur l’économie numérique et l’amélioration du climat
      des affaires adaptée aux besoins spécifiques des femmes, leur offrant des
      opportunités significatives, en particulier pour les jeunes femmes.

  •   Investir dans l’économie de la "Greentech" pour le déploiement des technologies
      écologiques en impliquant les femmes, visant à réduire l'empreinte carbone et à
      promouvoir l'utilisation des énergies renouvelables, ouvrant ainsi de nouvelles voies
      professionnelles pour les femmes.

  •   Développer l'économie circulaire dans ses stratégies de développement économique
      et industriel, pour favoriser des emplois durables pour les femmes. Cela comprend la
      promotion de l'innovation technologique, le soutien aux petites et moyennes
      entreprises engagées dans des pratiques durables, la création de zones industrielles
      écologiques, la réduction de la dépendance aux ressources importées et la
      préservation de l'environnement et de la biodiversité.

❖ Encourager des métiers innovants et l’entrepreneuriat chez les femmes

  •   Investir dans la formation des nouveaux métiers numériques attrayants pour les
      femmes pour préparer l’ère de l’automatisation tels que la création de contenu,
      l'ingénierie en cybersécurité, l’analyse de données, les spécialistes en intelligence
      artificielle et en machine learning, l’expertise en UX/UI design et les architectes
      Cloud.

  •   Encourager activement les femmes à s'orienter vers ces carrières grâce à des bourses
      et des mentors féminins dans ces domaines.




                                               99
  •   Développer des programmes de formation et d’accompagnement à l’entrepreneuriat
      adaptés aux femmes, tant en contenu qu'en mode de déploiement. En offrant des
      formations sur mesure pour répondre aux besoins spécifiques des femmes
      entrepreneures, tenant compte de leurs compétences, de leurs expériences et de
      leurs aspirations. Le déploiement de ces programmes devrait être flexible et adapté
      aux contraintes des femmes entrepreneures. Cela pourrait impliquer la mise en place
      d'horaires aménagés, de formations en ligne ou à distance, et la fourniture de
      ressources et de soutien à distance pour permettre aux femmes de suivre les
      formations, tout en jonglant avec leurs responsabilités familiales et professionnelles.
      L’implication des conjoints dans ces programmes peut avoir un impact significatif sur
      le succès et la pérennité de leurs entreprises, favorisant ainsi une meilleure
      compréhension et une plus grande collaboration au sein du foyer.

  •   Formaliser les initiatives entrepreneuriales des femmes en levant les entraves d’ordre
      administratif, réglementaire et fiscal, pour faciliter la création et la croissance des
      entreprises dirigées par des femmes, via la révision des procédures administratives
      et la simplification des réglementations et des incitations fiscales appropriées, pour
      encourager les femmes à entreprendre et à développer leurs activités sur le long
      terme.

❖ Renforcer le cadre juridique et réglementaire du travail des femmes

  •   Appliquer la Convention 100 de l'OIT sur l'équité salariale entre les femmes et les
      hommes, en renforçant les mécanismes de contrôle de l'application de la législation
      sociale pour garantir son efficacité.

  •   Adopter des réformes législatives recommandées par l'OIT pour encadrer et
      sécuriser le travail indépendant, le travail à domicile et les formes de travail qui
      émergent en dehors de tout cadre législatif, et qui peuvent améliorer
      significativement les conditions de travail des femmes, et renforcer leur autonomie
      économique.

  •   Ratifier certaines conventions internationales en faveur des femmes telles que la
      Convention (n° 190) de l’OIT sur la violence et le harcèlement et la Convention du
      Conseil de l’Europe sur la prévention et la lutte contre la violence à l’égard des
      femmes et la violence domestique (Convention d’Istanbul).

  •   Intégrer la dimension genre dans l’agenda du dialogue social (négociations
      collectives, politiques de rémunération, horaires de travail, politiques de conciliation
      travail-vie personnelle, réforme des régimes de retraite, politique de protection
      sociale).




                                              100
4. Mettre en place des stratégies de santé publique qui répondent aux défis en matière
   sanitaire

          En vue de faire face aux défis émergents de santé publique et pour améliorer les
   conditions de vie des femmes en réduisant les iniquités de santé, les axes d’orientations
   des politiques publiques, sont au nombre de trois : l'intégration des déterminants
   sociaux de la santé dans la législation, l'extension de la protection sociale en incluant de
   nouvelles prestations de soins pour les femmes, et le renforcement de la vigilance et la
   sécurité sanitaire face aux nouvelles épidémies.

❖ Intégrer les déterminants sociaux de la santé pour améliorer la santé des femmes

  •   Elaborer une loi relative à la santé publique, intégrant les déterminants sociaux de la
      santé, avec des mécanismes de gouvernance pour une action intersectorielle efficace
      sur les déterminants sociaux de la santé visant à réduire les inégalités en la matière.

  •   Accélérer la régionalisation de l'offre de soins en instituant des groupements
      sanitaires territoriaux et des programmes médicaux locaux, pour répondre aux
      besoins des femmes au niveau de chaque région.

  •   Garantir une répartition juste et équitable des ressources humaines en santé et des
      infrastructures de soins, en introduisant de nouveaux modes de travail, pour des
      fonctions sanitaires innovantes adaptées aux besoins différenciés des femmes, et un
      mécanisme d’incitation financière pour les médecins exerçant dans les espaces
      périphériques du pays.

  •   Renforcer la pénalisation de la violence à l’égard des femmes pour réduire de manière
      drastique les violences sexuelles, morales et physiques.

❖ Appuyer l’extension de la protection sociale globale et une santé publique inclusive au
  Maroc

  •   Appuyer la généralisation du chantier de la protection sociale avec une approche
      holistique reliant les questions sociales, politiques, économiques, culturelles et civiles
      en raison de l’indivisibilité, de l’interdépendance et de l’interrelation des droits. La
      mise en œuvre d’une politique coordonnée et harmonieuse, basée sur les principes
      de non-discrimination, de solidarité et de cohésion sociale durable, rétablissant le lien
      entre les politiques de prévoyance sociale (réformes de retraites, généralisation des
      allocations familiales, généralisation de l’AMO) et l’implémentation efficiente du
      Registre Social Unifié, permettra de renforcer la confiance institutionnelle.

  •   Assurer la prise en charge par le système de protection sociale, de la procréation
      médicalement assistée (PMA) et des nouvelles méthodes contraceptives, pour
      répondre aux nouveaux besoins sanitaires liés aux droits à la santé sexuelle et
      reproductive des femmes.

  •   Promouvoir les consultations médicales à domicile et à distance en facilitant l'accès
      à des services d'assistance médicalisée pris en charge par les assurances, pour
      répondre aux besoins des femmes dans un cadre flexible et adapté à leur emploi du
      temps.

                                               101
  •   Développer des services d’accompagnement post accouchement, liés à la maternité,
      pris en charge par l’AMO pour faciliter la réintégration professionnelle des mères, en
      tenant compte de leurs nouvelles responsabilités familiales.

❖ Renforcer la vigilance et la sécurité sanitaire face aux nouvelles épidémies

  •   Prendre des mesures urgentes pour réduire l’impact de la pollution atmosphérique
      et sensibiliser les femmes aux risques associés, afin de diminuer les maladies
      respiratoires et la mortalité liée à ce fléau au Maroc.

  •   Etablir un cadre de suivi-évaluation intégré pour collecter systématiquement des
      données sur les déterminants sociaux de la santé. Cet outil permettra de renforcer le
      système statistique national en données désagrégées par sexe et soutenir la
      recherche sur les iniquités en santé, pour générer des données probantes et orienter
      les politiques de santé équitables.

  •   Développer une politique publique, pour améliorer la santé mentale et le bien être
      des personnes en situation de vulnérabilité, qui répondra aux besoins spécifiques des
      femmes.

  •   Adopter une politique spécifique de lutte contre la violence numérique, pour
      protéger les victimes, en intégrant les attaques cyber-physiques et les nouvelles
      formes de discrimination en ligne. Les manipulations telles que les deep fakes
      représentent un défi émergent de troubles de santé mentale, ce qui nécessite une
      action décisive pour préserver l'intégrité des individus.

  •   Investir massivement dans le système de santé et généraliser la télémédecine pour
      renforcer les services de santé destinés aux femmes dans le monde rural, en prenant
      un certain nombre de mesures dont les plus importantes sont, d'encourager les
      professionnels à exercer en milieu rural et de garantir la sécurité des médicaments
      grâce à une politique pharmaceutique juste et équitable.

5. Mettre en place des systèmes de gouvernance accompagnant la transformation
   sociale

           Dans cette ère d'hyper-connectivité, la transformation numérique est en train de
   redéfinir le monde à une vitesse fulgurante. Cela n’est pas sans conséquence sur les
   systèmes de gouvernance qui sont appelés à évoluer de manière substantielle, sous
   peine de devenir inopérants. La lente intégration des femmes dans les systèmes de
   gouvernance, notamment aux fonctions supérieures, est un sujet très préoccupant, et
   ce malgré les mesures mises en place pour leur en faciliter l’accès, illustrant les
   difficultés rencontrées pour s’investir pleinement dans ces fonctions.

         Les axes d’orientations des politiques publiques sont au nombre de deux : faire
   évoluer le droit pour accélérer le changement et transformer les institutions.




                                             102
❖ Moderniser le droit pour accélérer le changement transformationnel

  •   Adopter une loi cadre pour l’égalité, la parité et la lutte contre les discriminations
      pour une mise en œuvre organisée et maîtrisée dans le temps des dispositions de la
      Constitution. Elle doit être accompagnée de stratégies visant la refondation du
      champ politique, la sensibilisation des entreprises aux bienfaits de la gouvernance
      paritaire, ainsi que d’une stratégie audiovisuelle de l’égalité.

  •   Harmoniser les textes de lois, concernant la femme, avec la Constitution et les
      conventions internationales ratifiées.

  •   Investir dans la réforme du système judiciaire pour améliorer l’accès des femmes à la
      justice et améliorer la pratique judiciaire au Maroc, et dans l’État de droit et d’une
      justice indépendante, pour assurer la mise en œuvre effective des nouveaux droits
      des femmes prévus par la Constitution.

  •   Réviser globalement le Code de la Famille, pour renforcer la cohésion familiale,
      éliminer les dispositions discriminatoires et instaurer une répartition équitable des
      responsabilités entre époux (l'intérêt supérieur de l'enfant, les droits de coparentalité
      en matière de tutelle, de filiation, de garde, l’héritage, et renforcer les mécanismes
      extrajudiciaires de règlement des conflits (la médiation).

  •   Réviser le Code Pénal et le Code de procédure pénale avec une approche juridico-
      analytique et légistique pour repenser la philosophie de l'action publique et
      combattre les stéréotypes de genre notamment d’amoindrir les délits mineurs,
      équilibrer l’autorité parentale, établir la paternité juridique, abolir la peine de mort,
      renforcer la présomption d’innocence et le droit à un procès équitable, et criminaliser
      les crimes financiers et technologiques.

  •   Intégrer dans les textes de lois, la gestion de crise, pour prendre en considération les
      besoins des femmes afin qu'elles bénéficient d'un accès équitable aux services de
      base.

❖ Transformer les institutions pour s'adapter aux besoins différenciés des femmes et des
  hommes

  •   Rationaliser et moderniser l'administration publique, centrée sur l’usager/usagère, en
      exploitant de manière effective les opportunités adaptées aux besoins des femmes,
      par la digitalisation, notamment la dématérialisation des procédures, et ce, pour
      moderniser ses processus et fournir efficacement des services accessibles à tous où
      qu’ils se trouvent sur le territoire national, en particulier aux femmes, et investir dans
      de nouvelles règles de gestion de carrière, basées sur la méritocratie.

  •   Opérationnaliser les instances constitutionnelles concernant la femme et la famille
      (APALD, CCEF).

  •   Adopter une charte politique et morale entre les partis afin d’intégrer la parité et
      l’égalité et redynamiser la vie partisane et politique, œuvrer au renforcement de la
      présence des femmes dans les partis politiques, au niveau des organisations
      syndicales et des institutions élues, restaurer la confiance dans l'action politique, et
      lier la responsabilité à l'obligation de reddition des comptes.

                                               103
•   Elaborer une politique foncière favorisant l'égalité d'accès des femmes au foncier et
    sécurisant les droits fonciers des femmes, et une gestion efficace des terres privées
    et domaniales.




                                           104
Conclusion
       La condition des femmes au Maroc se caractérise par une évolution positive
depuis l’accession du Royaume chérifien à l’indépendance. Si les acquis en la matière
sont indéniables, les dynamiques sociétales en cours démontrent néanmoins le besoin
de plus en plus pressant d’une nouvelle génération de réformes. Projeter la société dans
le 21ème siècle consiste à consolider les efforts entrepris en faveur du renforcement de
la cohésion sociale, pour un Maroc plus inclusif et égalitaire et un changement de
société en toute harmonie.
        Le dépassement des retards enregistrés tout autant que la prise en compte des
défis émergents seront de nature à créer les conditions nécessaires d’un futur
potentiellement vertueux, caractérisé par la qualité du capital humain et du lien social
solide, dans un système socio-économique en pleine évolution, à l’horizon 2050, soit
en une génération. La femme étant un acteur central de la société, et son évolution
l’une des meilleures mesures des progrès accomplis, l’amélioration de son statut dans la
société constitue une condition sine qua non pour atteindre ces objectifs.
       Il est par conséquent nécessaire de lever les contraintes et obstacles qui
entravent son épanouissement et sa participation à la construction de la société
marocaine du futur. La prise en charge des nœuds leviers identifiés dans cette étude y
contribuera dans une grande mesure.
       En inventant des politiques publiques adaptées, convergentes et coordonnées,
le pays dispose des ressources nécessaires pour amorcer une dynamique forte
d’intégration des femmes et de dépassement des nœuds existants. Investir dans la
culture de l’égalité, en s’appuyant sur les valeurs authentiques de l’identité marocaine
dans sa diversité, permettra une transformation culturelle apte à changer les mentalités
et lever les tabous liés aux stéréotypes persistants.
        Mener une stratégie de politique familiale cohérente et renforcée consolidera la
cellule familiale et contribuera à renforcer le lien social de base. Préconiser et mettre
en œuvre des politiques de l’emploi socialisées assurera la fluidité et l’efficacité de sa
participation au développement économique.
      Investir dans le bien-être et la santé des femmes créera les conditions idoines
pour une société épanouie et dénuée de violence.
       Modifier les structures des systèmes de gouvernance en y intégrant les
dimensions égalitaire et paritaire leur donnera plus de force, de créativité et
d’effectivité, et fera émerger un leadership féminin capable de relever les défis du futur,
dans une société équilibrée et inclusive.
       Une telle approche, en s’appuyant sur les germes de changement présents dans
la société- l’intégration des nouvelles technologies et de l’intelligence artificielle,
l’ouverture du Maroc au monde et les changements dans les pratiques des femmes- est
porteuse d’opportunités réelles et à notre portée pour consolider la démocratie, réduire
les inégalités systémiques et ouvrir de nouveaux horizons dans la ligne des aspirations
exprimées par Sa Majesté Le Roi Mohammed VI.




                                           105
Liste des illustrations

Figure 1: Perception des chefs de ménages de l’importance de l’école selon le milieu de résidence   21
Figure 2: Scores moyens des élèves en mathématiques et sciences, selon le genre                     21
Figure 3: Evolution du taux d’activité par genre en %                                               22
Figure 4: Évolution du taux de chômage par genre %                                                  23
Figure 5: Durée moyenne des activités selon le nombre d’enfants dans le ménage et le sexe           27
Figure 6: Evolution du taux du sous-emploi par genre %                                              30
Figure 7: L’entreprenariat, poids par genre (18 ans et plus en %)                                   30



Liste des tableaux

Tableau 1: Représentation des femmes aux élections communales                                       33
Tableau 2: Représentation des femmes aux élections législatives                                     33




                                                 106
Acronyme

AMO          Assurance Maladie Obligatoire
ANAM         Agence Nationale de l'Assurance Maladie
APALD        Autorité pour la Parité et la Lutte contre toute forme de Discrimination
BAD          Banque Africaine de Développement
BBC          British Broadcasting Corporation
BSG          Budgétisation Sensible au Genre
CCFE         Conseil Consultatif de la Famille et de l'Enfance
CCJAS        Conseil Consultatif de la Jeunesse et de l'Action Associative
CEDAW        Convention sur l’Elimination de toute forme de Discrimination à l’égard des Femmes
CESE         Conseil Economique Social et Environnemental
CERD         Convention Internationale sur l’Elimination de toutes les formes de Discrimination
             Raciale
CIDE         Convention Internationale relative aux Droits de l’Enfant
CNCMPTH      Commission Nationale de Coordination des Mesures de Lutte et de Prévention
             contre la Traite des êtres Humains
CNESAF       Commission Nationale pour l’Égalité entre les sexes et l’Autonomisation de la Femme
CNDH         Conseil National des Droits de l'Homme
CNPCFVV      Commission Nationale pour la Prise en Charge des Femmes Victimes de Violence
CSEFRS       Conseil Supérieur de l'Education, de la Formation et de la Recherche Scientifique
CSPJ         Conseil Supérieur du Pouvoir Judiciaire
DGCL         Direction générale des collectivités locales
EPCI         Etablissements publics de coopération intercommunale
EINA         Entrepreneurship, Innovations and Advice for North Africa
ENPSF        Enquête Nationale sur la Population et la Santé Familiale
HACA         Haute Autorité de la Communication Audiovisuelle
HCP          Haut-Commissariat au Plan
GISSR        Green Inclusive Smart Social Regeneration
ICRAM        Initiative Concertée pour le Renforcement des Acquis des Marocaines
IMM          Institution du Médiateur du Royaume
INDH         Initiative Nationale pour le Développement Humain
IPE          Indemnité pour la Perte d’Emploi
IPHAE        Instituto Para el Hombre, Agricultura y Ecología
IRES         Institut Royal des Etudes Stratégiques
MEF          Ministère de l’Economie et des Finances
MSISF        Ministère de la Solidarité, de l’Insertion Sociale et de la Famille
MSPS         Ministère de la Santé et de la Protection Sociale
NEET         Not in Education, Employment, or Training
OCDE         Organisation de Coopération et de Développement Economiques
ODD          Objectifs de Développement Durable
OIT          Organisation Internationale du Travail
OMD          Objectifs du Millénaire pour le Développement
ONDE         Observatoire National des Droits de l'Enfant
ONDH         Observatoire National du Développement Humain
ONMT         Observatoire National du Marché du Travail
ONU FEMMES   Agence des Nations Unies pour l'égalité des sexes et l'autonomisation des femmes
PGE          Plan Gouvernemental pour l'Égalité
PME          Petites et moyennes entreprises
PMI          Petites et moyennes industries
PMP          Présidence du Ministère Public
SMAG         Salaire Minimum Agricole Garanti
SNRT         Société Nationale de Radiodiffusion et de Télévision
SFI          Société Financière Internationale
UE           Union Européenne
UNFPA        Fonds des Nations Unies pour la Population


                                         107
Glossaire
Al maqâsid : Dans le droit musulman et plus particulièrement dans le domaine des Usûl al-
fîqh, « Maqâsid Ash Shari’a » prennent leurs racines dans les injonctions textuelles du Coran
et de la sunna mais correspondent aux idéaux et aux les objectifs de ces injonctions, qui
s'intéressent moins aux mots et sentences du texte qu'au but et propos recommandés. C’est
ainsi que les savants de l’époque « classique », notamment Al Ghazali, ont déterminé cinq
finalités à préserver par-dessus tout et ceci de manière formelle : la préservation de la
religion, la préservation de la vie, de la raison, des biens matériels et de sa descendance.
D’autres savants ont pu parfois rajouter d’autres finalités comme la préservation de la dignité
de l’homme. Chaque fatâwâ rendue se doit donc de prendre en compte ces finalités.
Cependant, il conviendra de juger de la nécessité de mettre en œuvre tel ou tel moyen pour
atteindre la finalité, c’est pourquoi le concept de Maqâsid est mis en œuvre conjointement
avec celui de « Maslaha » (170).

’aql (‫ )عقل‬: Littéralement ‘’raison’’, dans la jurisprudence, les facultés intellectuelles sont
utilisées pour trouver des solutions juridiques, définir les « lois religieuses » la charia dans les
cas où on ne trouve pas la réponse explicitement dans le Coran, ni dans la Sunna. Cet effort
intellectuel a été traduit par « raisonnement dialectique ».

Attaques cyber-physiques sont des actions délibérées et malveillantes effectuées à travers
des réseaux informatiques, dans le but de causer des dommages aux données et aux individus
qui les manipulent. L'analyse des systèmes cyber-physiques repose sur deux niveaux de
modélisation hiérarchique. Les recherches se concentrent d'abord sur la partie cyber pour
détecter les attaques malveillantes, puis sur la partie physique pour élaborer un schéma
global de commande capable de tolérer les imprévus. Les systèmes cyber-physiques, ou CPS,
représentent une nouvelle catégorie de systèmes qui résultent de la fusion des systèmes
embarqués, connectés à leur environnement physique via des capteurs et des actionneurs,
et aux réseaux mondiaux tels qu'Internet, avec ses données et ses services. Les CPS se
distinguent par leurs capacités, leur adaptabilité, leur évolutivité, leur résilience, leur sécurité
et leur convivialité supérieures (171).

Architecte Cloud : est un expert du cloud computing, il travaille dans l’optimisation des
systèmes : data centers, infrastructure des réseaux, outils numériques et solutions logicielles.
Il est responsable de leur organisation, de leur stockage, de leur sécurité, de leur évolution
et même de leur consommation d’énergie.
Le métier d’architecte du cloud est assez récent, l’expertise en architecture cloud permet
d’organiser les solutions numériques pour augmenter les performances technologiques de
l’entreprise, qui ont des répercussions sur la croissance générale (172).

Barrières socioculturelles : Elles sont le reflet de normes, croyances et pratiques enracinées
dans la diversité ethnique, linguistique et religieuse du pays. Elles sont traduites par les
attentes traditionnelles envers les rôles et les responsabilités des hommes et des femmes, les
pressions sociales et familiales pour que les filles se marient jeunes, les interprétations
restrictives de la religion peuvent façonner les attitudes. Ces barrières impactent plus les
femmes que les hommes (173).




                                                108
Blockchain : (“chaîne de blocs” en français) est une technologie émergente de stockage et de
transmission de l’information, réalisée de manière décentralisée et adoptée de manière
innovante par diverses industries. La blockchain évolue de manière autonome, sans organe
de contrôle : les utilisateurs sont autorisés à modifier cette base de données à tout moment
(ajouter des informations, vérifier une transaction…), seulement après avoir été
préalablement identifiés par un système cryptographique (174).

Centres pédagogiques ouverts (öppen fritidsverksamhet) : Les centres pédagogiques
ouverts sont accessibles aux enfants accompagnés d’un adulte, ils servent de supplément aux
autres services de garde. Dans certains quartiers défavorisés, ils ont une fonction sociale (175).

Chiqaq : est une nouvelle forme de divorce qualifiée dans la traduction française de divorce
« pour raison de discorde » (articles 94 à 97 du code de la famille). Dans lequel, la femme,
désireuse de mettre fin au mariage présente au tribunal une demande de divorce pour chiqaq.
Le tribunal est obligé dans ce cas d'accepter et de prononcer le divorce dans un délai
maximum de six mois à compter de la demande en tenant « compte de la responsabilité de
chacun des époux dans les causes du divorce pour évaluer la réparation du préjudice subi par
l'époux lésé » (Code famille)

Choubha : Sont les rapports sexuels entre femme et homme par erreur, ou viol, selon l’article
155 du Code de la Famille. Lorsqu’une femme est enceinte suite à des rapports sexuels par
erreur (Choubha) et donne naissance à un enfant, pendant la période comprise entre la durée
minimum et la durée maxima de la grossesse, la filiation paternelle de cet enfant est établie à
l’égard de l’auteur de ces rapports. Cette filiation paternelle est établie par tous moyens de
preuve légalement prévus (Code de la famille).

 Cleantechs : « clean technologie », le terme signifie « technologie propre » en français. Il fait
référence aux technologies et des modèles commerciaux connexes qui offrent des
rendements compétitifs aux investisseurs et aux clients tout en apportant des solutions aux
défis mondiaux (176).

Coding : En français c’est la programmation, appelée aussi codage dans le domaine
informatique, elle désigne l'ensemble des activités qui permettent l'écriture des programmes
informatiques. C'est une étape importante du développement de logiciels (177).

Crèches familiales (familjedaghem) : Les crèches familiales sont ouvertes aux enfants de 0 à
12 ans. Des assistantes maternelles agréées reçoivent les enfants à leur domicile. Ce mode
de garde est plus répandu dans les zones rurales que dans les zones urbaines (178).

Cybercriminalité : est un terme général désignant la multitude d'activités criminelles réalisées
à l'aide d'un ordinateur, d'un réseau ou d'autres dispositifs numériques. Elle englobe un large
éventail d'activités illégales perpétrées par des cybercriminels, telles que le piratage, le
phishing, l'usurpation d'identité, les ransomwares et les attaques par malware, entre autres.
Cette forme de criminalité transcende les frontières physiques, avec des criminels, des
victimes et des infrastructures techniques présents à travers le monde. Grâce à l'exploitation
des vulnérabilités de sécurité, aussi bien chez les particuliers que dans les entreprises, la
cybercriminalité prend de multiples formes et évolue constamment (179).

Deep fakes : est un enregistrement vidéo ou audio réalisé ou modifié grâce à l'intelligence
artificielle. Ce terme fait référence non seulement au contenu ainsi créé, mais aussi aux
technologies utilisées. Le mot deepfake est une abréviation de ‘’Deep learning’’ et "Fake", qui
peut être traduit par "fausse profondeur". En fait, il fait référence à des contenus faux qui
sont rendus profondément crédibles par l'intelligence artificielle (180).

                                               109
Design thinking : est une approche créative et centrée sur l'utilisateur pour résoudre les
problèmes et stimuler l'innovation. Cette approche met l'accent sur la compréhension
profonde des besoins des utilisateurs, la génération d'idées créatives, la création de
prototypes et le test itératif. Le Design Thinking favorise l'empathie, la collaboration
multidisciplinaire et l'expérimentation pour développer des solutions qui répondent
véritablement aux besoins des utilisateurs. Il s’agit donc d’une méthode d’intelligence
collective encourage également à remettre en question les hypothèses, à repenser les
problèmes de manière holistique et à adopter une approche itérative pour parvenir à des
résultats efficaces (181).

Développeur d'applications mobiles : effectue la réalisation technique et le développement
informatique d'applications pour mobiles, smartphones et autres tablettes. Il peut s'agir de la
création d'une application de toutes pièces, de l'adaptation d'un site web à l'une de ces plates-
formes, ou encore de l'optimisation d'une application déjà existante (182).

Discriminations intersectorielles : La définition de l’article 1 de la Cedaw introduit de façon
explicite le concept de discriminations intersectionnelles, lequel a été progressivement pris
en compte par plusieurs instruments juridiques internationaux qui considèrent que les
discriminations fondées sur le sexe ou le genre sont indissociablement liées à d’autres
facteurs, ce qui n’est pas sans affecter le bien-être des femmes et des filles, leur éducation,
leur santé, leur autonomie ou leur participation à la vie publique. Les discriminations se
manifestent de manière directe et/ou indirecte. Elles peuvent consister en des actes
volontaires et intentionnels, faciles à identifier, mais également se manifester de manière plus
insidieuse, au travers de stéréotypes, de normes sociales déséquilibrées et d’une répartition
inégalitaire du pouvoir, des ressources et des possibilités (183).

Domotique : (du latin domus, maison, et informatique) c’est l’ensemble des techniques qui
permettent de contrôler, de programmer et d’automatiser une habitation. Elle regroupe et
utilise ainsi les domaines de l’électronique, de l’informatique, de la télécommunication et des
automatismes. Elle permet de programmer la plupart des appareils et dispositifs électriques
de la maison, depuis l’éclairage et le chauffage jusqu’aux équipements audiovisuels et
électroménagers, en passant par l’ouverture des fenêtres. Elle facilite également le contrôle
de l’habitation en gérant les systèmes d’alarme, les préventions incendie, ou encore la
température au sein des pièces (184).

Doxing : est l'acte de révéler des informations personnelles en ligne, telles que le nom réel,
l'adresse, le lieu de travail, le numéro de téléphone ou des données financières, sans le
consentement de la personne concernée. Les attaques de doxing peuvent prendre diverses
formes, allant de nuisances mineures telles que des faux enregistrements sur des sites web
ou des commandes de nourriture non sollicitées, à des actions beaucoup plus dangereuses
comme le harcèlement familial ou professionnel, l'usurpation d'identité, les menaces et le
harcèlement physique (185).

Economie circulaire : est un modèle de production et de consommation qui consiste à
partager, réutiliser, réparer, rénover et recycler les produits et les matériaux existants le plus
longtemps possible afin qu'ils conservent leur valeur. De cette façon, le cycle de vie des
produits est étendu afin de réduire l'utilisation des matières premières et la production de
déchets (186).




                                               110
Economie-monde : désigne une économie formant un espace autonome, capable pour
l’essentiel de se suffire à lui-même et auquel ses liaisons et ses échanges intérieurs confèrent
une certaine unité organique. A ne pas confondre avec l’économie mondiale qui concerne
l’économie du monde pris dans sa globalité (187).

Enfant-roi : désigne des enfants qui se comportent comme s’ils étaient rois et que les autres
(amis, parents, famille) sont leurs sujets, devant répondre à leurs volontés et caprices.
L’enfant-roi à de la difficulté à tolérer de se faire dire non et réagit mal lorsqu’on tente de lui
mettre des limites, si minces soient-elles.

El Kol : Répudiation par le mari à la demande de la femme et moyennant compensation (188).

El ked wa saaya : constitue la part des acquets post mariage qui doit revenir à la femme en
cas de décès de l’époux ou de divorce, ce principe est conditionné du dépôt de preuve selon
le Code de la famille (189).

Expert en UX/UI design : c‘est un métier qui demande à la fois une compréhension de
l’humain, et des aptitudes en conception de produits. La profession est non seulement riche,
variée, stimulante, mais aussi en demande. Elle permet d’évaluer la qualité de l’interaction
entre l’utilisateur et le produit, l’UX Design permet de faire coïncider les besoins de
l’entreprise et ceux des utilisateurs finaux (190).

Extrême pauvreté : Condition caractérisée par une incapacité aigüe à répondre à ses besoins
primaires, y compris la faim, l'eau potable, les infrastructures sanitaires, la santé, la sécurité
d'un logement, l'éducation et l'information. Elle ne dépend pas que du niveau de revenu mais
aussi de l'accès aux services. Une personne vit en condition d’extrême pauvreté si elle ne
dispose pas de revenus nécessaires pour satisfaire ses besoins alimentaires essentiels définis
sur la base de besoins caloriques minimum (1800 calories par jour et par personne (OMS)).

Fîqh (‫ )فقه‬: Littéralement : "Compréhension". D'un point de vue juridique, c'est la science
fondée sur les méthodes de déduction des règles normatives à partir des sources islamiques
(Coran, Sounnah). L'effort d'interprétation d'un savant (‘âlim) à partir de ces sources est
l'ijtihad. Mais contrairement à la Charia qui relève de la loi divine, le fîqh (ou jurisprudence
islamique) relève d'un effort intellectuel humain. Le faqîh étant le juriste (191).

Génération Alpha : est le groupe démographique qui succède à la génération Z, née à partir
de 2010, avec la montée en puissance des tablettes et des smartphones, cette génération est
la première à grandir entourée de technologie dès son plus jeune âge. Elle est souvent
considérée comme la plus à l’aise avec la technologie, une familiarité innée avec les écrans
numériques et les interfaces tactiles (192).

Génération X : désigne les personnes nées entre 1966 et 1980 (+ de 56 ans)

Génération Y : correspond aux personnes nées entre 1980 et 1995, constituée des « digital
natives » ; elle est née dans un contexte d’automatisation, elle va se différencier des X en
repensant le monde et l’entreprise autour du marketing et du digital. Par définition, les
Millennials ou génération Y, sont entrées dans l’âge adulte à l’arrivée d’Internet (193).

Génération Z : se compose des personnes nées entre la fin des années 1990 et la fin des
années 2000. Ce public, désigné aussi par le terme de Zillenials, a succédé aux Milléniaux.
C’est une génération hyper connectée, avec les smartphones et les réseaux sociaux. Des
jeunes technophiles, que ce soit au regard de la scolarité, du travail, de la vie sociale, des
loisirs, de la culture ou de la consommation (194).

                                               111
Greentech : Technologie verte : désigne l'utilisation des technologies vertes et énergies
renouvelables. Son objectif est de mettre l’innovation numérique au service de la protection
de l’environnement. Elle s’attaque à des problématiques telles que la pénurie de ressources,
la décarbonation de l'énergie et la promotion d’une économie responsable (195).

Hacking : est l’acte de malveillance numérique qui consiste à exploiter une ou plusieurs
vulnérabilités (techniques, logiques, humaines ou organisationnelles) d’un système ou d’une
entité en vue d’en contourner les protections légitimes et d’y accéder afin d’atteindre des
objectifs tels que sabotage, espionnage, vol ou manipulation d’information (196).

Ijtihâd (‫ )اجتهاد‬: Littéralement, le terme Ijtihâd signifie « l’effort ». Au fil du temps, il prit le sens
particulier « d’effort de réflexion ». Il s'agit donc d'un effort d’interprétation de la Shari’a (de
réflexion et de recherches) effectué par un juriste musulman qualifié (faqîh, ouléma) soit pour
extraire une loi ou une prescription de sources scripturaires peu explicites, soit pour formuler
un avis juridique circonstancié en l’absence de textes de référence dans les sources de la loi
musulmane (Le Coran et les Hadiths). Ce principe se place en général après les deux sources
scripturaires incontournables, le Coran et la Sunnâ (Hadiths), mais se trouve surtout à la base
du qiyas (raisonnement analogique) et du consensus (ijmâ’) (197).

Indice de pauvreté multidimensionnel : (IPM – ou MPI en anglais pour Multidimensional
Poverty Index) est un indicateur statistique élaboré en 2010 par l'Oxford Poverty and Human
Development Initiative (OPHI) et utilisé par le Programme des Nations Unies pour le
Développement (PNUD) pour mesurer les inégalités et la pauvreté dans le monde. L’indice
appréhende les privations à travers trois dimensions (qui sont aussi celles prises en compte
par l’Indicateur de développement humain – IDH) : le niveau de vie, la santé et l'éducation.
La privation dans ces trois dimensions est évaluée à l’aide de 10 indicateurs : 2 indicateurs
pour mesurer le niveau d'éducation (nombre d’années de scolarité et taux de scolarisation), 2
indicateurs pour appréhender la santé (malnutrition et mortalité infantile) et 6 indicateurs
pour évaluer le niveau de vie (logement, sanitaires, accès à l'eau potable et à l'électricité,
combustible de cuisson, possession de matériel de transport et de communication).

Insécurité alimentaire : Les personnes sont en situation d’insécurité alimentaire modérée
lorsqu’elles sont incertaines de leur capacité à obtenir de la nourriture et qu’elles soient
contraintes de réduire, à certains moments de l’année, la qualité et/ou la quantité de
nourriture qu’elles consomment par manque d’argent ou d’autres ressources. L’insécurité
alimentaire grave fait référence à des situations dans lesquelles les individus ont épuisé leurs
réserves alimentaires, ont connu la faim et, au degré le plus avancé, sont restés plusieurs
jours sans manger. (FAO)

Machine learning : (apprentissage automatique) est une branche de l'intelligence artificielle
permettant aux machines d’apprendre sans avoir été préalablement programmées
spécifiquement à cet effet et qui implique l'utilisation d'algorithmes pour découvrir des
schémas récurrents, ou « patterns », dans des ensembles de données. Ces données peuvent
prendre diverses formes, telles que des chiffres, des mots, des images ou des statistiques, et
tout ce qui peut être stocké numériquement peut être utilisé comme données pour le
machine learning. Le Machine Learning est explicitement lié au Big Data, étant donné que
pour apprendre et se développer, les ordinateurs ont besoin de flux de données à analyser,
sur lesquelles s’entraîner (198).




                                                  112
Mariage coutumier : (mariage par la Fatiha) : Le mariage coutumier n’est pas reconnu par le
Code de la famille et ne donne donc lieu à aucun effet. Le mariage coutumier, ne permet pas
d’avoir par un acte de mariage, ce qui impacte la difficulté pour les époux de prouver leur
union conjugale, la perte des droits de la femme en cas de divorce ou encore des droits
conjugaux en cas de décès de l’un des conjoints, la difficulté pour les enfants de jouir de leurs
droits civiques (199).

Moudawana : Code de la famille au Maroc

Pensée systémique : la pensée systémique émerge dès le XIXè siècle, c’est une approche
holistique de l’analyse qui se concentre sur la façon dont les éléments constitutifs d’un système
sont interdépendants et sur la façon dont les systèmes fonctionnent dans le temps et dans le
contexte de systèmes plus vastes. Elle contraste avec l’analyse traditionnelle, (pensée
analytique ou linéaire) qui étudie les systèmes en les décomposant en leurs éléments distincts
(200)
      .

Procréation médicalement assistée (PMA) : c’est un ensemble de procédés qui permettent
la fusion d'un ovule et d'un spermatozoïde humains sans relations sexuelles, par une
intervention médicale (insémination artificielle ou fécondation in vitro avec transfert de
l'embryon dans l'utérus maternel) (201).

Principe de coparentalité : ce principe implique que le père et la mère soient parents à égalité,
dès lors qu'ils ont une filiation paternelle et maternelle légalement établies. Il désigne
l'exercice en commun de l'autorité parentale avec les enfants.

Programme Tayssir : est un programme gouvernemental mis en place par le ministère de
l'éducation afin de réduire le phénomène du décrochage scolaire notamment dans les zones
rurales, en octroyant des transferts monétaires conditionnels aux tuteurs et leur montant
varie en fonction du nombre d'enfants.

Services de garde publics (förskola ou daghem) : Les centres d’accueil préscolaires (förskola
ou daghem) sont ouverts toute l’année et ont des horaires flexibles pour mieux s’accorder
avec les besoins des parents (202).

Solidarités à base clanique : sont utilisées pour faire référence à toute solidarité en lien avec
un clan, c'est-à-dire un groupe de personnes réunies autour d'un chef, partageant les mêmes
valeurs, parfois de la même famille (203).

Tamaghribite : est ainsi définie juridiquement, par le préambule de la Constitution ‘’le
Royaume du Maroc entend préserver, dans sa plénitude et sa diversité, son identité nationale
une et indivisible. Son unité, forgée par la convergence de ses composantes arabo-islamique,
amazighe et saharo-hassanie, s’est nourrie et enrichie de ses affluents africain, andalou,
hébraïque et méditerranéen. La tamaghribite, c’est aussi le thé à la menthe autour duquel
s’exprime l’hospitalité, le malhoun qui enchante les soirées, les ahwash et ahidous, les chants
soufis, le culte des saints qui parsème les paysages de blancs marabouts, les moussems qui
rassemblent petits et grands, riches et pauvres, réalisant ainsi une autre valeur, l’inclusion
(204)
      .

Taux de divortialité : le rapport de divorces prononcé au nombre de mariages actés dans
l’année.




                                              113
Télémédecine : facilite la communication entre le patient et un ou plusieurs professionnels
de santé, ainsi qu'entre plusieurs professionnels de santé, grâce aux nouvelles technologies.
(OMS, 1997). Les cinq principaux actes de télémédecine sont la téléconsultation, la
téléexpertise, la télésurveillance, la télé-assistance et la régulation médicale.

Terres soulaliyates : Soulaliya en arabe est le féminin pluriel du mot soulali utilisé pour
nommer une personne appartenant à une collectivité ethnique possédant des terres
collectives et dont les membres sont liés par une généalogie commune (ou soulala). Les terres
collectives sont régies par une série de textes législatifs dont le plus important est le Dahir de
1919 qui organise la tutelle administrative de ces biens collectifs et en réglemente la gestion
et l’aliénation. En se référant à la fois aux textes de lois et à l’ensemble des règles coutumières
propres à chaque collectivité, ces derniers établissent les listes des ayants droit, gèrent la
résolution de conflits et exécutent les décisions du Conseil de tutelle (205).

Trolling : est l’acte de semer le trouble dans les commentaires de publications sur Internet
pour atteinte à une réputation ou de diffuser de fausses informations. Dans les cas les plus
inoffensifs, les trolls sont simplement agaçants. Mais dans les cas les plus graves, ils
alimentent une cabale diffamatoire, voire propagent des fakes news. Il a souvent une portée
beaucoup plus large, surtout lorsque des personnalités publiques et des entreprises sont
visées (206).

Usûl al-fîqh (‫ )أصول الفقه‬: Science des fondements de la loi islamique qui expose les sources
ainsi que les principes et la méthodologie au moyen desquels les règles du droit et de la
jurisprudence islamique sont déduites et extraites de ces sources (207).
Wilaya : la tutelle matrimoniale.




                                               114
Bibliographie

  (1) Organisations des Nations Unies. (1995). Déclaration et Programme d’action de Beijing :
       Quatrième Conférence mondiale sur les femmes.
  (2) https://www.unwomen.org/sites/default/files/Headquarters/Attachments/Sections/CSW/BP
       A_F_Final_WEB.pdf
  (3) Organisation des Nations Unies. (1995). Déclaration de Beijing et Programme d'action
       https://www.un.org/fr/conf/beijing/beijing-declaration-and-platform-for-action.
  (4) Nations Unies. (2015). Objectifs du Millénaire pour le développement : Rapport 2015
       https://www.un.org/fr/millenniumgoals/reports/2015/pdf/rapport_2015.pdf,
       rapport_2015.pdf (un.org).
  (5) Nations Unies (2022). Progrès vers la réalisation des objectifs de développement durable, gros
       plan sur l’égalité des sexes 2022. https://doi.org/10.18356/9789210018395.
  (6) Nations Unies (2023), Progrès vers la réalisation des objectifs de développement durable, gros
       plan sur l’égalité des sexes 2023. https://doi.org/10.18356/9789210029063.
  (7) Nations Unies (2022). Progrès vers la réalisation des objectifs de développement durable, gros
       plan sur l’égalité des sexes 2022. https://doi.org/10.18356/9789210018395.
  (8) Idem, op citée, p 10.
  (9) Glacier, O. (2015). La trace des femmes dans l’histoire du Maroc. Relations, (777), 35–37. Parmi
       les figures féminines d’envergure, elle cite Tin Hinan, reine des Touaregs entre 439 et 533,
       Zaynab al-Nafzawiyya, reine de l’empire almoravide (1055-1147), Chamsi Az-Ziwawiya qui
       régnait sur les Bani Yznaten à Ziwawa dans le Rif actuel, Sayyida Al-Horra (1493-1562) qui a
       gouverné Tétouan et le nord-ouest du Maroc pendant plus de 30 ans, Sahaba Er-Rahmania
       ambassadrice au XVIe siècle auprès de l’empire ottoman et qui a aidé son fils à fonder la dynastie
       saadienne, ou encore Khnata bent Bakkar (1662-1742) qui était conseillère de son conjoint, le
       sultan Moulay Ismaïl, pendant un demi-siècle et qui a dirigé par la suite le Maroc pendant 16 ans
       en tant que régente. Sans compter l’apport de Fatima Fihria qui a créé la première université au
       monde, ou celui de Malika El Fassi, signataire du Manifeste de l’indépendance.
  (10) Chevalier-Caron Christine (2017), Femmes et éducation au Maroc à l’époque coloniale (1912-
       1956). https://histoireengagee.ca/femmes-et-education-au-maroc-a-lepoque-coloniale-1912-
       1956/.
  (11) Chevalier-Caron Christine (2017), op citée.
  (12) Son Altesse Royale la Princesse Lalla Aicha. (1947, April 11). Discours historique à Tanger.
       [Discours].
  (13) Organisation des Nations Unies. (1995). Déclaration et Programme d'action de Beijing.
       https://www.un.org/fr/conf/beijing/beijing-declaration-and-platform-for-action et Nations
       Unies. (1994). Programme d’Action de la Conférence internationale sur la population et le
       développement.        https://www.unfpa.org/sites/default/files/event-pdf/icpd_eng_0.pdf,       et
       Nations       Unies.    (1993).   Déclaration      et    Programme       d’action   de     Vienne.
       https://www.ohchr.org/Documents/ProfessionalInterest/vienna.pdf.
  (14) Nations Unies (2022). 17 objectifs pour sauver le monde. Objectifs de développement durable.
       https://www.un.org/sustainabledevelopment/fr/objectifs-de-developpement-durable.
  (15) Union Africaine. (2015). L’Afrique 2063 que nous voulons, synthèse du premier Plan Décennal
       de         l’Agenda        2063.        https://au.int/sites/default/files/documents/33126-doc-
       11_an_overview_of_agenda_book_french.pdf.
  (16) Organisation des Nations Unies. (1993). Convention sur l’élimination de toute forme de
       discrimination                  à               l’égard                 des               femmes.
       https://treaties.un.org/doc/publication/unts/volume%201243/volume-1243-i-20378-f.pdf.
  (17) Conseil National des Droits de l'Homme. (s.d.). La pratique conventionnelle du Maroc en matière
       des droits de l’Homme : d’importants acquis et des défis à relever.
       https://www.cndh.org.ma/fr/bulletin-d-information/la-pratique-conventionnelle-du-maroc-en-
       matiere-des-droits-de-lhomme.




                                                 115
(18) Maroc. (2023). Rapport valant 19ème et 21ème rapports périodiques sur la mise en œuvre de la
     CERD [Rapport du gouvernement], Maroc. (2021). Rapport initial sur la mise en œuvre de la
     Convention internationale pour la protection de toutes les personnes contre les disparitions
     forcées [Rapport du gouvernement], Maroc. (2022). Rapport valant 5ème et 6ème rapports
     périodiques sur la mise en œuvre de la CEDAW [Rapport du gouvernement], Maroc. (2022).
     Rapport à mi-parcours sur l’état d’application des recommandations issues du 3ème cycle de
     l’Examen périodique universel et du 4ème cycle de l’examen périodique universel [Rapport du
     gouvernement].
(19) Conseil National des Droits de l'Homme. (2004). Avis consultatif du Conseil National des Droits
     de l'Homme concernant l’harmonisation du Code pénal marocain en matière de lutte contre la
     haine, la discrimination et la violence ; et Chambre des Représentants du Maroc. (2023). Saisine
     du Conseil Économique, Social et Environnemental par la Chambre des Représentants en 2023
     aux fins d’élaborer un avis sur la problématique du mariage des mineurs et sur son impact sur la
     situation socio-économique des filles.
(20) Décret no 2-17-740 (juillet 2018), Bulletin officiel n° 6722 (juillet 2018).
(21) Cette commission a été remplacée par la Commission Ministérielle pour l’égalité présidée par le
     chef du Gouvernement qui avait pour mission de suivre les différents programmes
     gouvernementaux de l’égalité.
(22) Nations Unies. (2015). Objectifs du Millénaire pour le développement : Rapport 2015.
     https://www.un.org/fr/millenniumgoals/reports/2015/pdf/rapport_2015.pdf, p 47 Rapport-
     national-2015.pdf.
(23) Ratification de la CEDAW avec des réserves sur l’article 2, le paragraphe 2 de l'article 9, le
     paragraphe 4 de l'article 15 et les articles 16 et 29.
(24) Cette institution est l’actuel Ministère de la Solidarité, de l’Insertion Sociale et de la Famille.
(25) Le lancement de la première campagne nationale de lutte contre la violence à l’égard des femmes
     intitulée "Non à la violence contre les femmes" Cette campagne organisée en partenariat avec
     l'UNFPA a réussi à "briser le silence", en sensibilisant largement à l'échelle nationale grâce à une
     diffusion étendue sur divers médias, y compris les médias audiovisuels et les spots publicitaires,
     stratégie-nationale-de-lutte-contre-la-violence-à-l'égard-des-femmes.pdf (social.gov.ma).
(26) Direction des Études et des prévisions financières. (2006). Étude comparative des Objectifs du
     Millénaire        pour        le       Développement            :      Données         de        1995.
     https://www.finances.gov.ma/Publication/depf/2006/5027_doc22.pdf.
(27) Ce plan a été élaboré à l’initiative de la Présidence du Ministère Public, en partenariat avec le
     Ministère de l’Éducation nationale, du préscolaire et des sports, le Ministère de la Santé et de la
     protection sociale, le Ministère de l’Intérieur (Conseils élus et INDH), le Ministère de la Solidarité,
     de l’Insertion sociale et de la famille, le Ministère des Habous et des Affaires islamiques, le
     Ministère de l’Équipement et de l’eau, le Conseil supérieur du Pouvoir judiciaire (CSPJ et le
     Ministère de la Justice.
(28) Ministère de la Réforme, de l’Administration et de la Fonction Publique (2016). Stratégie
     d’institutionnalisation de l’égalité entre les sexes dans la fonction publique, Ministère de
     l’Éducation nationale, la formation professionnelle et l’enseignement supérieur (2021). Stratégie
     nationale de la formation professionnelle 2021-2030, le Ministère de l’Inclusion Économique, de
     la Petite Entreprise, de l’Emploi et des Compétences (2015). Stratégie Nationale pour l’Emploi
     du Royaume du Maroc 2015-2025.
(29) Ministère de la Solidarité, du Développement Social, de l’Egalité et de la Famille (2002). Stratégie
     nationale de lutte contre les violences à l’égard des femmes et des filles, Ministère de la Santé
     (2017). Programme national de prise en charge des femmes et des enfants victimes de violences.
(30) Nations Unies. (2015). Objectifs du Millénaire pour le développement : Rapport 2015.
     https://www.un.org/fr/millenniumgoals/reports/2015/pdf/rapport_2015.pdf p 47.
(31) Haut-Commissariat au Plan (HCP). (2023). Population et Développement au Maroc, 30 ans après
     la Conférence du Caire de 1994, Rapport Général, p 91.
(32) Programme gouvernemental 2021- 2026.
(33) RES (2024).Séminaire de présentation des principales conclusions de la 3eme édition de
     l’enquête nationale sur le lien sociale’’ volet famille et femme’’, le 21 FEVRIER 2024,P 21,
     https://ires.ma/fr/publications/rapports-generaux/les-principaux-resultats-de-la-troisieme-
     edition-de-lenquete-nationale-sur-le-lien-social-se-rapportant-au-lien-familial-et-la-condition-
     de-la-femme
(34) Haut-Commissariat au Plan (HCP). (2023). Femmes marocaines en chiffres, p 16.

                                                 116
(35) Haut-Commissariat au Plan(HCP). (2023). Les Indicateurs sociaux du Maroc, Edition 2023, p 20.
(36) IRES (2024)., op citée.
(37) Chekrouni, N., & Jaidi, A. (2024). Le Code de la famille marocain : réalités et perspectives de
     réformes. Policy Center for the New South. P 18.
(38) IRES (2024)., citée p 30
(39) Centre Stratégique Marocain de Développement. (2021). Nouveau modèle de développement
     (p. 74) [Rapport général]. https://csmd.ma/documents/Rapport_General.pdf.
(40) Conseil National des Droits de l'Homme. (2004). Avis consultatif sur l'harmonisation du Code
     pénal marocain en matière de la lutte contre la haine, la discrimination et la violence [Avis
     consultatif], https://www.ccdh.org.ma/ Avis consultatif sur l'harmonisation du Code pénal
     marocain en matière de la lutte contre la haine, la discrimination et la violence | Conseil National
     des Droits de l'Homme (ccdh.org.ma).
(41) Commission nationale de prise en charge des femmes victimes de violence,2021, p 48.
(42) IRES (2024).Séminaire de présentation des principales conclusions de la 3eme édition de
     l’enquête nationale sur le lien sociale’’ volet famille et femme’’, P 21,
(43) Comité pour l'élimination de la discrimination à l'égard des femmes (CEDAW). (2020). Rapport
     valant cinquième et sixième rapports périodiques soumis par le Maroc en application de l'article
     18 de la Convention.
(44) Ministère de l'Éducation Nationale (2023). Bilan du département de l'éducation nationale et du
     préscolaire en chiffres et indicateurs au titre de l’année scolaire 2022/2023, p.1.
(45) Idem, op citée.
(46) Soit un taux de 4%, dont 36.804 au primaire (2%), 62.748 (environ 7.5%) au secondaire collégial
     et 30.042 (environ 5.5%) au secondaire qualifiant.
(47) Ministère de l'enseignement supérieur et de la recherche scientifique (MESRS). (2023).
    L'enseignement supérieur en chiffres 2022-2023
(48) Ministère de l'Éducation Nationale. (2016). Programme International pour le Suivi des Acquis des
     élèves de 7 année.
                ème


(49) Observatoire National du Développement Humain (ONDH). (2019). Enquête Panel de ménages
     de l’Observatoire National du Développement Humain. https://www.ondh.ma/fr/enquete-
     panel-de-menage.
(50) HRC/47/26, Conseil des droits de l’Homme, quarante-septième session 21 juin-9 juillet 2021
     Point 3 de l’ordre du jour. Rapport de la Rapporteuse spéciale sur la violence contre les femmes,
     ses causes et ses conséquences
(51) Conseil Economique Social et Environnemental (2016). Les dimensions sociales de l’égalité entre
     les femmes et les hommes : constats et recommandations.
(52) Banque Mondiale (2021). Tendances et déterminants de la participation des femmes à la vie
     active au Maroc : Une première analyse exploratoire.
(53) Banque Mondiale (2021). Op citée.
(54) Haut-Commissariat au Plan (2017). Évolution de la taille moyenne des ménages par milieu de
     résidence : 1960-2050.
(55) Haut-Commissariat au Plan (HCP). (2022). Bouchra EL BIDAOUI, les brefs du plan, Femme et
     écart d’âge entre les époux au Maroc, N° 19 • 11 octobre 2022
(56) Haut-Commissariat au Plan (HCP). (2023). Femmes marocaines en chiffres, p 16.
(57) Rapport du Conseil supérieur du pouvoir judiciaire de 2024
(58) Institut Royal des Études Stratégiques (IRES). (2024). Séminaire de présentation des principales
     conclusions de la 3eme édition de l’enquête nationale sur le lien sociale’’ volet famille et femme’’,
     le 21 FEVRIER 2024,P 21, https://ires.ma/fr/publications/rapports-generaux/les-principaux-
     resultats-de-la-troisieme-edition-de-lenquete-nationale-sur-le-lien-social-se-rapportant-au-
     lien-familial-et-la-condition-de-la-femme
(59) Haut-Commissariat au Plan (HCP). (2023). Femmes marocaines en chiffres, p 27.
(60) Haut-Commissariat au Plan (HCP). (2023). Population et Développement au Maroc, 30 ans après
     la Conférence du Caire de 1994, Rapport Général, p 34.
(61) Haut-Commissariat au Plan (2012). Enquête Nationale sur l’Emploi du Temps.
(62) El Marizgui, H., Ezzrari, A., & Soudi, K. (2021). Mesure multidimensionnelle de la pauvreté
     féminine au Maroc
(63)       Haut-Commissariat au Plan (2022). Activité, emploi et chômage. Résultats
    annuels 2022.


                                                117
(64) Haut-Commissariat au Plan (HCP). (2023). Femmes marocaines en chiffres, p 153.
(65) HCP 2024"Inégalités des salaires hommes-femmes en milieu urbain Rôle de la discrimination
     sexiste".
(66) Haut-Commissariat au Plan (HCP). (2023). Femmes marocaines en chiffres, p 154.
(67) Observatoire National du Développement Humain (2020). Les discriminations intersectionnelles
     des femmes au Maroc.
(68) Agence National Assurance Maladie (2022). RAPPORT D’ACTIVITÉS 2022 -Branche Amo Au
     service de la généralisation de l’AMO de base, p 49, https://anam.ma/anam/wp-
     content/uploads/2023/04/RAPPORT-DACTIVITES-2022.pdf.
(69) Ministère de la Santé et de la Protection sociale, OMS, (2023), Analyse des iniquités en santé au
     Maroc
(70) Fondation Lalla Salma - Prévention et traitement des cancers, première journée
    nationale du registre des cancers sous le thème « Surveillance du cancer au Maroc :
    Passé - Présent et Futur », 21 Janvier 2023, Casablanca
(71) Haut-Commissariat au Plan (HCP). (2023). Population et Développement au Maroc, 30 ans après
     la Conférence du Caire de 1994, Rapport Général, p 29.
(72) Les projections de la population et des ménages entre 2014 et 2050, HCP, 2017
(73) Trends in maternal mortality 2000 to 2020, Estimates by WHO, UNICEF, UNFPA, World Bank
     Group and UNDESA/ Population Division, 2023
(74) Ministère de la Santé et de la Protection sociale, OMS, (2023), Analyse des iniquités en santé au
     Maroc.
(75) Haut-Commissariat au Plan (HCP). (2023). Femmes marocaines en chiffres, p 22.
(76) Augmentation du nombre d’autorisations de mariages des filles mineures depuis 2004 jusqu’à
     2011.
(77) INSAF, (2014). Mariage précoce au Maroc, négation des droits de l’enfant. Eléments de
     plaidoyer.
(78) Ministère de la Santé et de la Protection sociale, OMS, (2023), Analyse des iniquités en santé au
     Maroc.
(79) Données Banque mondiale
(80) Haut-Commissariat au Plan (HCP). (2023). Femmes marocaines en chiffres, p 163.
(81) Baudot, P., & Bley, D. (1997). La contraception en milieu rural marocain : Bilan d’enquêtes de
     terrain.    Conception,       Naissance     et     Petite    Enfance     Au     Maghreb,     95–103.
     https://doi.org/10.4000/books.iremam.2900. CONTRACEPTION
(82) Ministère de la santé. (2018). Enquête nationale sur la population et la santé familiale.
(83) Cible pour l’objectif 5 est « Garantir la participation entière et effective des femmes et leur accès
     en toute égalité aux fonctions de direction à tous les niveaux de décision, dans la vie politique,
     économique et publique ».
(84) Maroc. (2011). Constitution du Royaume du Maroc. L’article 30 « des dispositions de nature à
     favoriser l’égal accès des femmes et des hommes aux fonctions électives ».
(85) Maroc. (2011). Constitution du Royaume du Maroc. L’article 146 relatif aux régions et aux
     collectivités territoriales stipule qu'une loi organique devra fixer « (…) les dispositions visant à
     assurer une meilleure participation des femmes au sein des Conseils territoriaux ».
(86) Haut-Commissariat au Plan (2023). La femme marocaine en chiffres.
(87) Organisation de Coopération et de Développement Économiques (2018). La Participation des
     femmes dans la vie politique au sein du parlement et des conseils élus au Maroc.
(88) Haut-Commissariat au Plan (2023). La femme marocaine en chiffres.
(89) Maroc. (2011). Constitution du royaume du Maroc. Article 26 « Tout parti politique œuvre à
     élargir et à généraliser la participation des femmes et des jeunes dans le processus de
     développement politique de la société. À cet effet, tout parti politique œuvre pour atteindre la
     proportion d’un tiers de participation des femmes dans ses organes dirigeants aux niveaux
     national et régional, dans le but de la réalisation, à terme et d’une manière progressive, du
     principe de parité entre les hommes et les femmes ».
(90) Haut-Commissariat au Plan (2023). La femme marocaine en chiffre.
(91) Enquête Gouvernance et Parité. (2022). Women on Boards in Morocco - Rapport de synthèse.
(92) Galland, O. (2004). Permanences et mutations du système de valeurs. Permanences,
     changements et enjeux pour l’avenir. Prospective Maroc 2030. Haut-commissariat au Plan.


                                                118
  (93) Institut Royal des Études Stratégiques (IRES). (2024). 3e édition de l’enquête nationale sur le lien
       social.
  (94) Maroc. (2011). Constitution du royaume du Maroc. Extrait du préambule.
  (95) Institut Royal des Études Stratégiques (IRES). (2022). Quel avenir de l’eau au Maroc ? Rapport
       de synthèse des travaux de la journée scientifique.
  (96) Forum économique mondial, rapport Global gender gap 2023. Le rapport révèle que le Maroc se
       positionne au 136ème rang. Il est devancé par d'autres pays de la région tels que la Tunisie
       (128ème rang) et l'Égypte (134ème rang). L’Indice de développement humain du Programme des
       Nations unies pour le développement (PNUD) classe le Maroc au 123ème rang en 2022. Enfin,
       en 2021, le Maroc a un Indice d'inégalité de genre de 0,683 point le plaçant dans la tranche des
       pays à ‘’développement humain moyen’’, au 123ème rang sur 191 pays (PNUD Rapport sur le
       développement humain 2021/2022 ‘’ Temps incertains, vies bouleversées : façonner notre
       avenir dans un monde en mutation’' Gender social norms index, Breaking Down Gender Biases,
       Shifting social norms towards gender equality,2023, p 32, gsni202303.pdf (undp.org)).
  (97) Hamdouch, B. et al. (2018), Enquête IMAGES sur les hommes et l’égalité des sexes menée dans
       la région de Rabat-Salé-Kénitra, Cairo and Washington, D.C.: UN Women and Promundo-
       US.,https://morocco.unwomen.org/sites/default/files/Field                                   Office
       Morocco/Documents/Publications/2018/07/Rapport Images-VF-WEB.pdf
  (98) Houria ALAMI M’CHICHI (2007), Le Code de la famille Perceptions et pratique judiciaire,
       Changement social et perceptions du nouveau Code de la famille.
  (99) HCP (2024), les indicateurs sociaux du Maroc Edition 2024, Haut-Commissariat au Plan, p 43,
       https://www.hcp.ma/downloads/?tag=Femme+marocaine+en+chiffres
  (100)         ENPSF (2018), Enquête Nationale sur la Population et la Santé Familiale, Ministère de la
       Santé,                                                                                      Rabat,
       https://www.unicef.org/morocco/media/1626/file/Enqu%C3%AAte%20Nationale%20sur%20
       La%20Population%20et%20la%20Sant%C3%A9%20Familiale%20(ENPSF%20-2018).pdf.
(101) Aboulkacem, E. (2008), Droit coutumier amazigh face aux processus d’institution et d’imposition
       de la législation nationale au Maroc, Organisation internationale du Travail,
       https://www.ilo.org/wcmsp5/groups/public/---ed_norm/---
       normes/documents/publication/wcms_100800.pdf.
(102) Malika Benradi, (2007), le Code de la famille, Perceptions et pratique judiciaire.
(103) Mohamed Tozy (2009), L’évolution du champ religieux marocain au défi de la mondialisation,
       Dans Revue internationale de politique comparée (Vol. 16), pages 63 à 81.
(104) Omar Azzimane (2013), La tradition juridique islamique dans l’évolution du droit privé marocain,
       le Maroc actuel : Une modernisation au miroir de la tradition ? Institut de recherches et d’études
       sur les mondes arabes et musulmans, Éditions du CNRS, 1993, p251-272,
       https://books.openedition.org/iremam/2411.
(105) Haut-Commissariat au Plan (2013). Mariage et divorce de la femme marocaine :
       tendances d'évolutions.
(106) Le rapport de divorces prononcé au nombre de mariages actés dans l’année.
(107) Rapport 2024, conseil supérieur de la police judiciaire.
(108) La loi n° 65.15 relative aux établissements de protection sociale et ses décrets d'application,
       publiée au B.O en 2018 vise à élargir la liste des services fournis aux bénéficiaires des
       établissements de protection sociale.
(109) Plateforme numérique « Gissr Amane » a pour but de faciliter les requêtes de prise en charge des
       femmes et des jeunes filles victimes de violence sous toutes ses formes et d'accéder aux services
       de prise en charge, en envoyant la demande directement par la personne concernée, par
       l'intermédiaire d'un tiers, d'une association, lien https://gissr-amane.social.gov.ma/.
(110) Ponthieux S. (2012), « La mise en commun des revenus dans les couples », Insee Première, n°
       1409.
(111) Haut-commissariat au Plan (HCP). (2024). Analyse intersectionnelle de la participation des
       femmes au marché́ du travail marocain.
(112) Banque Africaine de Développement, Ministère des Finances, EINA (2023). Enquête nationale
       sur le profil entrepreneurial du Maroc.
(113) Banque Africaine de Développement, idem, op citée.
(114) Omayma Achour (2019) Réforme des retraites au Maroc :29 années de réflexion, concertation,
       recherche d’un consensus, La Lettre de l’Observatoire des Retraites, N°26
       https://www.calameo.com/books/00271172965ff7174a330.

                                                  119
  (115) Alami M. (2001) Femmes et marché du travail au Maroc, Communication présentée au XXIVe
        Générale de la population (UISFP)Salvador, Brésil.
  (116) World Health Organization Regional (WHO) Office for the Eastern Mediterranean (EMRO).
        2015. - Regional consultation on reducing health inequities in the Eastern Mediterranean.
  (117) Wagstaff A. Pauvreté et inégalités dans le secteur de la santé, de la politique à l’action, Article
        publié en anglais dans Bulletin of the World Health Organization, 2002, 80(2), 97–105.
  (118) Thomas Piketty, « le Capital au XXIe siècle » (2015) et « inégalités et redistributions,
        développements théoriques récents » (1994).
  (119) HCP (2020). Enquête sur l’impact du coronavirus sur la situation économique, sociale et
        psychologique des ménages. Note de synthèse des principaux résultats.
  (120) ONDH (2017). Enquête ménage
  (121) Ministère de la Santé et de la Protection sociale, OMS, (2023), Analyse des iniquités en santé au
        Maroc
  (122) HCP. Les Brefs du Plan N° 6 - 11 Novembre 2018
  (123) Ministère de la Santé et la protection sociale, OMS, (2009), la démographie médicale et
        paramédicale à l’Horizon 2025.
  (124) Une mesure de la santé mentale tel que l’indice unifié de bien-être australien qui intègrerait les
        différentes composantes du bien-être (émotionnelle, psychologique et sociale) permettrait
        d’apprécier le niveau global de santé mentale de la population, et mesurerait l’impact de
        l’ensemble des politiques publiques sur le bien-être de la population. Par exemple, l’indice unifié
        de bien-être australien (The Australian Unity Wellbeing) qui mesure la qualité de vie à travers le
        bien-être personnel et le bien-être national ; l’échelle du bienêtre psychologique (Psychological
        well-being scale) qui évalue le fonctionnement psychologique positif ; l’échelle du bien-être
        social (The Social Well-Being Scale) qui permet de mesurer la prospérité des individus dans leur
        vie sociale par le Well-being.
  (125) CESE (2020), la santé mentale et les causes de suicide au Maroc, p 11.
        https://www.cese.ma/media/2023/01/Rapport-sante%CC%81-mentale.pdf
  (126) HCP, Enquête sur l’impact de la pandémie de COVID-19 sur la situation économique, sociale et
        psychologique des ménages, avril 2020 : https://www.hcp.ma/file/215933/
  (127) Agoub M, Moussaoui D, Battas O., “Prevalence of postpartum depression in a Moroccan sample”,
        Archives of Women’s Mental Health, 2005 May, Vol 8 N°1, pp.37-43.
  (128) Ministère de la santé et la protection sociale : Document du plan Santé 2025.
  (129) MSPS, PNSPCFEVV, 2017, Programme, prise en charge des femmes et enfants victimes de
        violence.
  (130) Evaluation des Systèmes Environnemental et Social, 2023, PAAIIS-ESES-versmars2023-
        compact.pdf.
  (131) MSPS, Stratégie de SSR, https://www.sante.gov.ma/Documents/2023/04/SNSSR%202021-
        2030.pdf.
  (132) Evaluation des Systèmes Environnemental et Social, 2023, PAAIIS-ESES-versmars2023-
        compact.pdf.
  (133) MSPS, Stratégie Nationale de la Santé des Adolescents et des Jeunes 2022-2030, 2023.
  (134) Promulguée par le Dahir n° 1-02-296 du 25 rejeb 1423.
  (135) Haut-Commissariat au Plan (HCP). (2023). Population et Développement au Maroc, 30 ans après
        la Conférence du Caire de 1994, Rapport Général.
  (136) Haut-Commissariat au Plan (HCP). (2023). Population et Développement au Maroc, 30 ans après
        la Conférence du Caire de 1994, Rapport Général, p 126.
  (137) Deloitte (2020), Diversité et inclusion : comment faire de l’inclusion un levier de transformation
        des organisations.
(138) Haut-commissariat au Plan (HCP). (2024). Analyse intersectionnelle de la participation des
        femmes au marché́ du travail marocain.
(139) Institut Royal des Études Stratégiques (IRES). (2020). Rapport stratégique : Vers un nouveau
        modèle de développement.
(140) Encyclopédie canadienne. (2020). Loi sur le multiculturalisme canadien. Repéré à
        https://www.thecanadianencyclopedia.ca/fr/article/loi-sur-le-multiculturalisme-canadien.
  (141) Arretche, M. (2004). Federalismo e políticas sociais no Brasil : problemas de coordenação e
        autonomia. São Paulo em Perspectiva, 18(2), 20.
  (142) IPHAN: http://www.iphan.gov.br.


                                                   120
(143) Anderson Orestes Cavalcante Lobato, La protection du patrimoine culturel au Brésil : la
      reconnaissance de la diversité culturelle, Revue Juridique de l’Ouest Année 2012 N-S 1 pp. 15-
      26, La protection du patrimoine culturel au Brésil : la reconnaissance de la diversité culturelle -
      Persée (persee.fr).
(144) Alves, E. P. M. (2010). Diversidade cultural, patrimônio cultural material e cultura popular : à
      Unesco e a construção de um universalismo global. Revista Sociedade e Estado, 25(3), 539-560.
(145) République Française, Loi du 24 juin 2020 visant à lutter contre les contenus haineux sur
      internet, https://www.vie-publique.fr/loi/268070-loi-avia-lutte-contre-les-contenus-haineux-
      sur-internet.
(146) Morel, N. (2001). Politique sociale et égalité entre les sexes en Suède. Revue des politiques
      sociales et familiales, 64, 65-79. Récupéré sur https://www.persee.fr/doc/caf_1149-
      1590_2001_num_64_1_952.
(147) Myrdal, A. (1971). Towards equality: The Alva Myrdal report to the Swedish social democratic
      party. Prisma.
(148) Sainsbury, D. (1999). Gender and welfare state regimes. Oxford University Press.
(149) Björnberg, U. (Ed.). (1996). Men’s family relations. Almqvist et Wiksell.
(150) Parental                           Leave                             Act                             1995)
      https://www.government.se/contentassets/d163a42edcea4638aa112f0f6040202b/sfs-
      1995584-parental-leave-act.
(151) Le congé parental a remplacé le congé de maternité et est ouvert aux deux parents dès le premier
      enfant, la mère gardant cependant son droit à un congé rémunéré dès soixante jours avant la
      naissance et vingt-neuf jours après.
(152) La durée du congé parental sera portée à seize mois (les trois derniers mois étant rémunérés au
      taux forfaitaire de base), et chaque parent bénéficiera de deux mois non transférables, toujours
      dans le but d’inciter les pères à participer plus activement à l’éducation de leurs enfants et aux
      tâches domestiques.
(153) Ce sont des jours rémunérés, que le père doit prendre dans les soixante jours suivant la venue à
      la maison d’un enfant.
(154) Collombet, C., & Math, A. (2020). Politiques d’accueil du jeune enfant et l’indemnisation du congé
      parental. Schémas nationaux d’articulation en Allemagne, en France et en Suède. Revue des
      politiques       sociales      et      familiales,       136-137,       83-90.         Récupéré         sur
      https://www.persee.fr/doc/caf_2431-4501_2020_num_136_1_3437.
(155) Bygren, M., & Duvander, A.-Z. (2006). Parents’ workplace situation and fathers’ parental leave
      use. Journal of Marriage and Family, 68(2), 363-372.
(156) Almqvist, A. L., & Duvander, A. Z. (2014). Changes in gender equality? Swedish fathers’ parental
      leave, Division of Childcare and Housework. Journal of Family Studies, 20(1), 19-27.
(157) Oberhuemer, P., & Schreyer, I. (Eds.). (2017). Early childhood workforce profiles in 30 countries
      with key contextual data. seepro-r. Munich. http://www.seepro.eu/ISBN-publication.pdf.
(158) Morel, N. (2001). Politique sociale et égalité entre les sexes en Suède. Revue des politiques
      sociales et familiales, 64, 65-79. Récupéré sur https://www.persee.fr/doc/caf_1149-
      1590_2001_num_64_1_952.
(159) Forum économique mondial, rapport Global Gender gap 2022.
(160) OCDE (2023), OECD Review of Gender Equality in Colombia, Éditions OCDE, Paris,
      https://doi.org/10.1787/a559fc5e-en.
(161) Mastercard Index of Women Entrepreneurs (MIWE), (2018), How targeted support for women-
      led     business      how       can     unlock       sustainable      economic         growth,       2018,
      https://www.mastercard.com/news/media/phwevxcc/the-mastercard-index-of-women-
      entrepreneurs.pdf
(162) https://www.acceleratingasia.com/programs/the-women-in-climatetech-and-sustainability-
      reverse-accelerator.
(163) AISS-Association Internationale de la Sécurité Sociale (2012), « Note de politique tirée de la stratégie de
       protection sociale en Afrique régimes de retraite » déc.
(164) AISS - Association Internationale de la Sécurité Sociale (2008), Rapport « Une sécurité sociale dynamique
       pour l’Afrique : une stratégie pour le développement Développements et tendances », p18.
(165) BONILLA G. A. (2005), « Les pensions Réformes récentes et expériences des régimes de pension La réforme
       des régimes publics de pensions : un survol chronologique des principaux apports au débat », op citée.
(166) GONZALES M. T. (2010), « Le revenu de dignité (Renta Dignidad) : un système de pension de vieillesse
       universel », p 22.


                                                      121
(167) BENITO P. (2008), « En Bolivie, Evo Morales instaure une rente universelle dès 60 ans », 12 février.
(168) S. GRONCHI ET S. NISTICÒ (2006), « Implementing the NDC theoretical model: a comparison of Italy and
      Sweden », in R. Holzmann et E. Palmer (éd.), Pension Reform: Issues and Prospect for Non-Financial Defined
      Contribution.
(169) BORDIGNON, M., S. GIANNINIET P. PANTHEGINI (2001), « Reforming Business Taxation: Lessons from
      Italy? », International Tax and Public Finance, no 8, pp191-210.
(170) Vie publique.fr, site réalisé par la Direction de l’information légale et administrative (DILA),
      rattachée aux services du Premier ministre).
(171) Cahiers de l’Islam. (2023), Revue d’étude sur l’islam et le monde musulman,
      https://www.lescahiersdelislam.fr/glossary/Maqasid-
      %D8%A7%D9%84%D9%85%D9%82%D8%A7%D8%B5%D8%AF_gw99.html.
(172) Olivier Jacq. (2021), Détection, analyse contextuelle et visualisation de cyber-attaques en temps
      réel : élaboration de la Cyber Situational Awareness du monde maritime. Cryptographie et
      sécurité [cs.CR]. Ecole nationale supérieure Mines-Télécom Atlantique, 2021.
      https://theses.hal.science/tel-03145173v1/document.
(173) Data science, répertoire des métiers. (2024), https://datascientest.com/
(174) Observatoire National du Développement Humain (2020). Les discriminations intersectionnelles
      des femmes au Maroc.
(175) Magazine de la prévention suisse de la cybercriminalité. (2024), Dossier Intelligence artificielle
      et        criminalité,       numéro          1,       2024,         https://www.skppsc.ch/fr/wp-
      content/uploads/sites/5/2024/04/psc_info_1_2024.pdf.
(176) Morel, N. (2001). Politique sociale et égalité entre les sexes en Suède. Op citée.
(177) Chambre de commerce du Québec. (2020) Plan d’action pour renforcer le secteur des
      technologies propres.
(178) Magazine de la prévention suisse de la cybercriminalité. (2024), op citée.
(179) Morel, N. (2001). Politique sociale et égalité entre les sexes en Suède. Op citée.
(180) Magazine de la prévention suisse de la cybercriminalité. (2024), op citée.
(181) Magazine de la prévention suisse de la cybercriminalité. (2024), op citée.
(182) ADOBE                       (2023),                      Réflexion                   conceptuelle,
      https://www.adobe.com/fr/creativecloud/design/discover/design-thinking.html
(183) Orientation pour tous. (2024), https://www.orientation-pour-tous.fr/metier/developpeur-euse-
      d-applications-mobiles,15652.html
(184) Observatoire National du Développement Humain (2020). Op citée.
(185) Les dossiers du Mag de la Domotique. Qu’est-ce que la domotique ? Définition et exemples
      d’applications,         https://www.lemagdeladomotique.com/dossier-1-domotique-definition-
      applications.html.
(186) Kaspersky. Le doxing : définition et explication, https://www.kaspersky.fr/resource-
      center/definitions/what-is-doxing,
(187) Parlement                                       Européen.                                  (2023),
      https://www.europarl.europa.eu/topics/fr/article/20151201STO05603/economie-circulaire-
      definition-importance-et-benefices
(188) Vincent Capdepuy, (2022) . 50 histoires de mondialisations, L'ordonnancement du monde, le
      rétrécissement du monde, le tournant de l’économie mondiale
(189) Marie-Claire Foblets, Mohamed Loukiliv. (2006), Dalloz Etudiant, Revue critique de droit
      international privé, p. 521, Mariage et divorce dans le nouveau Code marocain de la famille :
      Quelles      implications    pour    les     Marocains      en     Europe?,    https://actu.dalloz-
      etudiant.fr/fileadmin/actualites/pdfs/RevDip2006-521.pdf.
(190) Edwige Rude-Antoine. (2010) Actualités du droit musulman : genre, filiation et bioéthique,
      Divorces au masculin et au féminin, Le mariage et le divorce dans le Code marocain de la famille.
      Le nouveau droit à l’égalité entre l’homme et la femme, p. 43-57,
      https://doi.org/10.4000/droitcultures.1961.
(191) Usabilis. (2023). Conseil UX et ergonomie digitale, https://www.usabilis.com.
(192) Cahiers de l’Islam (2023), op citée.
(193) Observatoire National du Développement Humain (2020). Op citée.
(194) Clara Landecy (2021), op citée.
(195) Clara Landecy (2021), op citée.
(196) Cozynergy (2023), https://www.cozynergy.com/conseils-subventions/la-green-tech-cest-quoi.



                                                    122
(197) Philippe WOLF. (2011), « Ambiguïtés et cyber-conflits », Colloque IMODEV « Cybercriminalité,
      cybermenaces          et      cyberfraudes        »,      Paris,     20        et      21       juin,
      https://cyber.gouv.fr/sites/default/files/IMG/pdf/Cyber_conflits_quelques_cles_de_comprehe
      nsion.pdf.
(198) Cahiers de l’Islam . (2023), op citée.
(199) Jérémy Robert. (2020) Machine Learning : Définition, fonctionnement, utilisations,
      https://datascientest.com/machine-learning-tout-savoir
(200) Stéphane Pap. Laïcité : la nouvelle frontière, Les mariages à la fātiḥa et le droit français, Revue
      du droit des religions, p. 129-140, https://doi.org/10.4000/rdr.648
(201) QRP International. (2024), Approche et pensée systémique c’est quoi ? Définition, origine et
      explications, https://www.qrpinternational.fr/blog/glossaire/approche-et-pensee-systemique-
      cest-quoi-definition-origine-et-explications/
(202) Guide de l’assistance médicale à la procréation (2020), www.agence-biomedecine.fr.
(203) Morel, N. (2001). Politique sociale et égalité entre les sexes en Suède. Op citée.
(204) Jacques Heers, Le Clan familial au Moyen Âge (1993), Chapitre IV - Solidarité des clans. Liens de
      voisinages, pages 137 à 177.
(205) Fouad Laroui. (2023), Qu’est-ce que la « tamaghrabit ».
(206) Yasmine Berriane. Inclure les « n’ayants pas droit » : Terres collectives et inégalités de genre au
      Maroc, p. 61-78, Pratique du droit et propriétés au Maghreb dans une perspective comparée,
      https://doi.org/10.4000/anneemaghreb.2546.
(207) Nolwenn Lorenzi Bailly et Claudine Moïse.Discours de haine et de radicalisation, (2023), ENS
      Éditions, Lyon, 10.4000/books.enseditions.43765
(208) Cahiers de l’Islam. (2023), op citée.




                                                  123
Annexe 1 : Matrice des nœuds

  1- La Matrice du nœud des normes sociales discriminantes qui exacerbent les disparités :




  2- La Matrice du nœud marché de l’emploi tendu et non inclusif :




                                              124
3- La Matrice du nœud des systèmes de gouvernance caractérisés par le déficit en termes d’égalité de
   genre et de parité




4- La Matrice du nœud des rapports déséquilibrés engendrés par la mutation de la famille




                                           125
  5- Nœud de l’iniquité en matière d’accès aux soins et les inégalités sociales de santé




Annexe 2 : Carte heuristique




                                               126
Annexe 3 : Fiche des ateliers
Fiche de l’atelier n° 1 sur le capital humain et l’autonomisation économique des femmes :




Liste des expert.e.s qui ont participé à l’atelier n°1 :

•   Fatima Agnaou, Professeure sociologue,
•   Abdessamad Sentissi, Expert en entrepreneuriat PME,
•   Saad Belghazi , Économiste expert emploi,
•   Ihssane Iraqi , Experte genre, Women in business program manager,
•   Mehdi Fakir, Economiste,
•   Alaoui Ouafa, Entrepreneure (AFEM),
•   Mohammed HAZIM, Expert en emploi,
•   Zakaria Fahim, Expert entreprenariat,
•   Aiman Cheragui, Expert jeunesse,
•   Youness EL ANSARI, Expert dans la législation et les conditions du travail.




                                                      127
Interactions lors de l’atelier : images du futur concernant l’usage de l’intelligence artificielle :




                                                     128
Fiche de l’atelier n° 2 sur les mutations sociales, les droits fondamentaux et la gouvernance :







                                    
"""
    conversation_history = StreamlitChatMessageHistory()  # Créez l'instance pour l'historique

    st.header("Explorez le rapport sur l’avenir de la femme marocaine à l’horizon 2050 à travers notre chatbot 💬")
    
    # Load the document
    #docx = 'PLF2025-Rapport-FoncierPublic_Fr.docx'
    
    #if docx is not None:
        # Lire le texte du document
        #text = docx2txt.process(docx)
        #with open("so.txt", "w", encoding="utf-8") as fichier:
            #fichier.write(text)

        # Afficher toujours la barre de saisie
    st.markdown('<div class="input-space"></div>', unsafe_allow_html=True)
    selected_questions = st.sidebar.radio("****Choisir :****", questions)
        # Afficher toujours la barre de saisie
    query_input = st.text_input("", key="query_key",placeholder="Posez votre question ici...", help="Posez votre question ici...")
    st.markdown('<div class="input-space"></div>', unsafe_allow_html=True)

    if query_input and query_input not in st.session_state.previous_question:
        query = query_input
        st.session_state.previous_question.append(query_input)
    elif selected_questions:
        query = selected_questions
    else:
        query = ""
    predefined_question = "Donnez-moi un résumé du rapport"

    loading_message = st.empty()

    if query :
        st.session_state.conversation_history.add_user_message(query) 
        # Vérifier si la question de l'utilisateur contient la question prédéfinie
        if predefined_question.lower() not in query.strip().lower():
        # Afficher le message de "Génération de la réponse" si la question est différente
            loading_message.text("Génération de la réponse...")
            st.markdown('<div class="loading-message"></div>', unsafe_allow_html=True)

        

        if "Donnez-moi un résumé du rapport" in query:
            summary="""Le rapport « L’avenir de la femme marocaine à l’horizon 2050 », publié par l’IRES en juillet 2024, dresse un état des lieux de la condition féminine au Maroc, entre avancées notables (réformes juridiques, accès à l’éducation, participation politique) et défis persistants (inégalités socio-économiques, discriminations culturelles, faible accès aux soins). Il identifie cinq nœuds majeurs à surmonter pour garantir l’égalité réelle entre les sexes et propose deux scénarios prospectifs : un scénario tendanciel de stagnation et un scénario souhaitable misant sur l’inclusion, l’autonomisation et la parité. Le rapport s’appuie également sur des expériences internationales réussies et recommande des politiques publiques ambitieuses dans les domaines de l’éducation, de l’emploi, de la santé et de la gouvernance pour faire de l’égalité femmes-hommes un levier de développement durable d’ici 2050."""
            st.session_state.conversation_history.add_ai_message(summary) 

        else:
            messages = [
                {
                    "role": "user",
                    "content": (
                        f"{query}. Répondre à la question d'apeés ce texte repondre justement à partir de texte ne donne pas des autre information voila le texte donnee des réponse significatif et bien formé essayer de ne pas dire que information nest pas mentionné dans le texte si tu ne trouve pas essayer de repondre dapres votre connaissance ms focaliser sur ce texte en premier: {text} "
                    )
                }
            ]

            # Appeler l'API OpenAI pour obtenir le résumé
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages
            )

            # Récupérer le contenu de la réponse

            summary = response['choices'][0]['message']['content']
           
                # Votre logique pour traiter les réponses
            #conversation_history.add_user_message(query)
            #conversation_history.add_ai_message(response)
            st.session_state.conversation_history.add_ai_message(summary) 
              
            #query_input = ""

            loading_message.empty()


 # Ajouter à l'historique
            
            # Afficher la question et le résumé de l'assistant
            #conversation_history.add_user_message(query)
            #conversation_history.add_ai_message(summary)

            # Format et afficher les messages comme précédemment
                
            # Format et afficher les messages comme précédemment
        formatted_messages = []
        previous_role = None
        if st.session_state.conversation_history.messages:
        # Parcourir les messages de manière inversée par paire (question, réponse)
            messages_pairs = zip(reversed(st.session_state.conversation_history.messages[::2]), 
                             reversed(st.session_state.conversation_history.messages[1::2]))

            for user_msg, assistant_msg in messages_pairs:
                role_user = "user"
                role_assistant = "assistant"
            
                avatar_user = "🧑"
                avatar_assistant = "🤖"
                css_class_user = "user-message"
                css_class_assistant = "assistant-message"
 
            # Formater et afficher la question de l'utilisateur et la réponse de l'assistant
                message_div_user = f'<div class="{css_class_user}">{user_msg.content}</div>'
                message_div_assistant = f'<div class="{css_class_assistant}">{assistant_msg.content}</div>'

                avatar_div_user = f'<div class="avatar">{avatar_user}</div>'
                avatar_div_assistant = f'<div class="avatar">{avatar_assistant}</div>'

                formatted_message_user = f'<div class="message-container user"><div class="message-avatar">{avatar_div_user}</div><div class="message-content">{message_div_user}</div></div>'
                formatted_message_assistant = f'<div class="message-container assistant"><div class="message-content">{message_div_assistant}</div><div class="message-avatar">{avatar_div_assistant}</div></div>'

                formatted_messages.append(formatted_message_user)
                formatted_messages.append(formatted_message_assistant)
          
        # Afficher les messages formatés
            messages_html = "\n".join(formatted_messages)
            st.markdown(messages_html, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
