# Generated by Django 2.0.2 on 2018-06-24 16:39

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import tagulous.models.fields
import tagulous.models.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('terms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('journal', models.TextField(blank=True, null=True)),
                ('issue', models.TextField(blank=True, null=True)),
                ('volume', models.TextField(blank=True, null=True)),
                ('title', models.TextField(blank=True, null=True)),
                ('year', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_text', models.CharField(blank=True, max_length=500, null=True)),
                ('citation', models.TextField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Definition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('defs', models.TextField()),
                ('defs_html', models.TextField(editable=False)),
                ('year', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('citeNumber', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'ordering': ['-year'],
            },
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('count', models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use')),
                ('protected', models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.CreateModel(
            name='Synonym',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('count', models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use')),
                ('protected', models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='synonym',
            unique_together={('slug',)},
        ),
        migrations.AlterUniqueTogether(
            name='discipline',
            unique_together={('slug',)},
        ),
        migrations.AddField(
            model_name='definition',
            name='discipline',
            field=tagulous.models.fields.TagField(_set_tag_meta=True, autocomplete_view='definition_discipline_autocomplete', help_text='This field splits tags on commas', initial='"Acoustics, Dynamics, and Controls", "Aerodynamics and Fluid Mechanics", "Aeronautical Vehicles", "Aerospace Engineering", "African Languages and Societies", "Agronomy and Crop Sciences", "Algebraic Geometry", "American Art and Architecture", "American Film Studies", "American Material Culture", "American Politics", "American Popular Culture", "American Studies", "Analytical Chemistry", "Ancient History (Greek and Roman through Late Antiquity)", "Ancient Philosophy", "Ancient, Medieval, Renaissance and Baroque Art and Architecture", "Animal Sciences", "Animal Sciences", "Anthropological Linguistics/Sociolinguistics", "Applied Linguistics", "Applied Mathematics", "Applied Mechanics", "Applied Statistics", "Aquaculture and Fisheries", "Artificial Intelligence/Robotics", "Asian Art and Architecture", "Astronomy and Astrophysics", "Astrophysics and Astronomy", "Atmospheric Sciences", "Atomic, Molecular and Optical Physics", "Behavior and Ethology", "Behavioral Economics", "Behavioral Neurobiology", "Biblical Studies", "Biochemical and Biomolecular Engineering", "Bioelectrical and neuroengineering", "Bioimaging and biomedical optics", "Biological Engineering", "Biological Psychology", "Biological and Chemical Physics", "Biological and Physical", "Biology and Biomimetic Materials", "Biomechanical Engineering", "Biomechanics and biotransport", "Biomedical Engineering and Bioengineering", "Biomedical devices and instrumentation", "Broadcast/Video Studies", "Byzantine and Modern Greek", "Cancer Biology", "Catalysis and Reaction Engineering", "Cell Biology", "Cell and Developmental Biology", "Cellular Physiology ", "Ceramic Materials", "Chemical Engineering", "Civil Engineering", "Civil and Environmental Engineering", "Classical Archaeology and Art History", "Classical Literature and Philology", "Clinical Psychology", "Cognition and Perception", "Cognitive Neuroscience", "Cognitive Psychology", "Communication Technology and New Media", "Community Psychology", "Comparative LiteratureEnglish Language and Literature", "Comparative Methodologies and Theories", "Comparative Nutrition", "Comparative Politics", "Comparative and Evolutionary Physiology", "Comparative and Historical Linguistics", "Complex Fluids", "Computational Biology", "Computational Engineering", "Computational Linguistics", "Computational Neuroscience", "Computer Engineering", "Computer Engineering", "Computer Sciences", "Computer and Systems Architecture", "Computer and Systems Architecture", "Computer-Aided Engineering and Design", "Condensed Matter Physics", "Construction Engineering/management", "Contemporary Art", "Continental Philosophy", "Control Theory", "Controls and Control Theory", "Cosmology, Relativity, and Gravity", "Criminology and Criminal Justice", "Critical and Cultural Studies", "Cultural History", "Dairy Science", "Data Storage Systems", "Databases/Information Systems", "Demography, Population, and Ecology", "Developmental Biology", "Developmental Neuroscience", "Developmental Psychology", "Digital Circuits", "Digital Communications and Networking", "Diplomatic History", "Discourse/Text Linguistics", "Discrete Mathematics and Combinatorics", "Dramatic Literature, Criticism and Theory", "Dynamic Systems", "Dynamics/Dynamical Systems", "Dynamics/Dynamical Systems", "Earth Sciences", "East Asian Languages and Societies", "Ecology and Evolutionary Biology", "Economic History", "Economic Theory", "Electrical and Computer Engineering", "Electrical and Electronics", "Electro-Mechanical Systems", "Electromagnetics and photonics", "Electronic Devices and Semiconductor Manufacturing", "Elementary Particles and Fields and String Theory", "Energy Systems", "Engineering Mechanics", "Engineering Physics", "Engineering Science and Materials", "Entomology Food Science", "Environmental Chemistry", "Environmental Engineering", "Environmental Health", "Environmental Health", "Environmental Health", "Environmental Microbiology and Microbial Ecology", "Environmental Sciences", "Ethics and Political Philosophy", "Ethnic Studies", "European Languages and Societies ", "Exercise Physiology", "Exercise Physiology", "External Galaxies", "Family, Life Course, and Society", "Feminist Philosophy", "Feminist, Gender and Sexuality Studies", "Feminist, Gender, and Sexuality Studies", "Film Studies", "First/Second Language Acquisition", "Fluid Dynamics", "Food Biotechnology", "Food Chemistry", "Food Microbiology", "Food Processing", "Forest Biology", "Forest Management", "Forestry and Forest Sciences", "French Linguistics", "French and Francophone Language and Literature", "French and Francophone Literature", "Fresh Water Studies", "Gender and Sexuality", "Gender, Race, Sexuality, and Ethnicity in Communication", "Genetics and Genomics", "Geographic Information Sciences", "Geometry and Topology", "Geophysics and Seismology", "Geotechnical Engineering", "German Language and Literature", "German Linguistics", "German Literature", "Graphics/Human Computer Interfaces", "Growth and Development", "Hardware Systems", "Harmonic Analysis and Representation", "Health Communication", "Health Psychology", "Heat Transfer, Combustion", "History of Art, Architecture and Archaeology", "History of Philosophy", "History of Religion", "History of Religions of Eastern Origins", "History of Religions of Western Origin", "History of Science, Technology, and Medicine", "Human Geography", "Human and Clinical Nutrition", "Immunology and Infectious Disease", "Immunology of Infectious Disease", "Immunoprophylaxis and Therapy", "Indo-European Linguistics and Philology", "Industrial Engineering", "Industrial Organization", "Industrial and Organizational Psychology", "Inequality and Stratification", "Information Science", "Inorganic Chemistry", "Integrated Biology", "Integrated Biomedical Sciences", "Intellectual History", "International Economics", "International Relations", "International and Community Nutrition", "International and Intercultural Communication", "Interpersonal/Small Group Communication", "Islamic World/Near East", "Journalism Studies", "Labor Economics", "Language Description/Documentation", "Language, Societies, and Cultures", "Latin American Languages and Societies", "Latin American Literature", "Latin American", "Linguistic Anthrolpology", "Literature in English, Anglophone (other than British Isles and North America)", "Literature in English, British Isles", "Literature in English, North America (other than ethnic and minority)", "Literature in English, North America, ethnic and minority", "Logic and Foundations", "Logic and foundations of mathematics", "Mass Communication", "Materials Chemistry", "Materials Science and Engineering", "Mechanical Engineering", "Mechanics of Materials", "Medicinal Chemistry", "Medicinal-Pharmaceutical Chemistry", "Medicine and Health", "Medieval History", "Membrane Science", "Microbial Physiology", "Military History", "Mineral Physics", "Models and Methods", "Modern Art and Architecture", "Molecular Biology", "Molecular Physiology", "Molecular and Cellular Neuroscience", "Molecular genetics", "Molecular, Genetic, and Biochemical Nutrition", "Molecular, cellular, and tissue engineering", "Motor Control", "Multi-Vehicle Systems and Air Traffic Control", "Music Theory", "Nanoscience and Nanotechnology", "Nanotechnology fabrication", "Nature and Society Relations", "Navigation, Guidance, Control and Dynamics", "Near Eastern Languages and Societies", "Neuroscience and Neurobiology", "Non-linear Dynamics", "Non-linear Dynamics", "Non-linear Dynamics", "Nuclear Engineering", "Number Theory", "Numerical Analysis and Computation", "Numerical Analysis/Scientific Computing", "Nutritional Epidemiology", "Ocean Engineering", "Oceanography and Atmospheric Sciences and Meteorology", "Operational Research", "Operations Research, Systems Engineering and Industrial Engineering", "Ordinary Differential Equations and Applied Dynamics", "Organic Chemistry", "Organizational Communication", "Partial Differential Equations", "Pathogenic Microbiology", "Performance Studies", "Personality and Social Contexts", "Petroleum Engineering", "Philosophy of Language", "Philosophy of Mind", "Philosophy of Science", "Physical Chemistry", "Physical Processes", "Physical and Environmental Geography", "Place and Environment", "Plant Biology", "Plant Breeding and Genetics", "Plant Pathology", "Plant Sciences", "Plasma and Beam Physics", "Political History", "Political Science", "Political Theory", "Politics and Social Change", "Polymer Chemistry", "Polymer Science", "Polymer and Organic Materials", "Population Biology", "Portuguese Literature", "Poultry (or Avian) Science", "Power and Energy", "Process Control and Systems", "Programming Languages/Compilers", "Propulsion and Power", "Psychology of Movement", "Public Administration", "Public Affairs", "Public Affairs, Public Policy and Public Administration", "Public Economics", "Public Health", "Public Policy", "Public Relations/Advertising", "Quantum Physics", "Race and Ethnicity", "Race, Ethnicity and post-Colonial Studies", "Regional Sociology", "Religious Thought/Theology/Philosophy of Religion", "Rhetoric and Composition", "Rhetoric and Composition", "Rural sociology", "Science and Technology Studies", "Semiconductor and Optical Materials", "Set Theory", "Signal Processing", "Slavic Languages and Societies", "Social Control, Law, Crime, and Deviance", "Social History", "Social Influence and Political Communication", "Social Psychology and Interaction", "Social Psychology", "Social and Cultural", "Sociology of Culture", "Software Engineering", "Soil Science", "South and Southeast Asian Languages and Societies", "Space Vehicles", "Spanish Linguistics", "Spanish Literature", "Spanish and Portuguese Language and Literature", "Speech and Rhetorical Studies", "Stars, Interstellar Medium and the Galaxy", "Statistical Methodology", "Statistical Theory", "Statistics and Probability", "Structural Biology", "Structural Biology", "Structural Engineering", "Structural Materials", "Structures and Materials", "Systems Biology", "Systems Engineering and Multidisciplinary Design Optimization", "Systems Engineering", "Systems Neuroscience", "Systems and Communications", "Systems and Integrative Physiology", "Systems and integrative engineering", "Tectonics and Structure", "Terrestrial and Aquatic Ecology", "The Sun and the Solar System", "Theatre History", "Theatre and Performance Studies", "Theory and Criticism", "Theory, Knowledge and Science", "Transport Phenomena", "Typological Linguistics and Linguistic Diversity", "United States", "Urban Studies and Planning", "Urban Studies", "VLSI and circuits: Embedded/Hardware Systems", "Womenís History", "Wood Science and Pulp/Paper Technology", "Work, Economy and Organizations", African, Algebra, Analysis, Anatomy, Anthropology, Archaeological, Asian, Astrodynamics, Bacteriology, Biochemistry, Biochemistry, Biochemistry, Biogeochemistry, Biogeochemistry, Biogeochemistry, Bioinformatics, Biology, Biomaterials, Biomechanics, Biomedical, Biometry, Biophysics, Biophysics, Biostatistics, Biostatistics, Biotechnology, Botany, Botany, Chemistry, Classics, Climate, Communication, Composition, Cosmochemistry, Cosmology, Criminology, Econometrics, Economics, Endocrinology, Epidemiology, Epistemology, Ergonomics, Esthetics, Ethics, Ethnomusicology, European, Evolution, Gender, Genetics, Genomics, Geochemistry, Geography, Geology, Glaciology, History, Horticulture, Immunity, Immunopathology, Instrumentation, Kinesiology, Legal, Linguistics, Macroeconomics, Manufacturing, Mathematics, Metallurgy, Metaphysics, Meteorology, Microbiology, Morphology, Music, Musicology, Nuclear, Nursing, Nutrition, OS/Networks, Oceanography, Optics, Paleobiology, Paleontology, Parasitology, Pathology, Pharmaceutics, Pharmacology, Pharmacology, Philosophy, Phonetics/Phonology, Physics, Physiology, Playwriting, Probability, Psycholinguistics/Neurolinguistics, Religion, Robotics, Semantics/Pragmatics, Sociology, Syntax, Theory/Algorithms, Thermodynamics, Toxicology, Toxicology, Tribology, Virology, Vulcanology, Zoology', space_delimiter=False, to='definitions.Discipline'),
        ),
        migrations.AddField(
            model_name='definition',
            name='synonym',
            field=tagulous.models.fields.TagField(_set_tag_meta=True, autocomplete_view='definition_synonym_autocomplete', help_text='This field splits tags on commas', initial='flair', space_delimiter=False, to='definitions.Synonym'),
        ),
        migrations.AddField(
            model_name='definition',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='definitions', to='terms.Term'),
        ),
        migrations.AddField(
            model_name='definition',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='definitions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='authors',
            name='definitions',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to='definitions.Definition'),
        ),
        migrations.AlterUniqueTogether(
            name='definition',
            unique_together={('user', 'defs')},
        ),
    ]
