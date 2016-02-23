import os
import re
import numpy as np
from settings import OUTPUT, CIRCOS
from settings import MONGODB as db
from Analysis.output import get_hgt
from Bio import SeqUtils


def safe_species_name(species_name):
    return re.sub('\W', '_', species_name)


def get_karyotypes(length_cutoff=1000):
    """
    Generate circos karyotypes for each species in database
    """
    outdir = os.path.join(OUTPUT, 'circos', 'karyotypes')
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    for species in db['genes'].distinct('species'):
        name = safe_species_name(species)
        with open(os.path.join(outdir, '{}_karyotype.txt'.format(name)), 'w+') as out_handle:
            color = [np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255)]
            for contig in db['genes'].find({'species': species, 'type': 'contig'}):
                if len(contig['dna_seq']) >= length_cutoff:
                    out_handle.write('chr - {0}-{1} {2} {3} {4} {5},{6},{7}\n'.format(
                        name,
                        contig['contig_id'],
                        contig['contig_id'],
                        '1',
                        len(contig['dna_seq']),
                        *color
                        )
                    )
                else:
                    break


def get_links(minimum_identity, minimum_length=100):
    outdir = os.path.join(OUTPUT, 'circos', 'links')
    if not os.path.isdir(outdir):
        os.makedirs(outdir)


    with open(os.path.join(outdir, '{}-{}-links.txt'.format(int(minimum_identity * 100), minimum_length)), 'w+') as out_handle:
        for s1, s2 in get_hgt(minimum_identity, minimum_length):
            s1_record = db['genes'].find_one({'_id': s1})
            s2_record = db['genes'].find_one({'_id': s2})

            s1_name = safe_species_name(s1_record['species'])
            s2_name = safe_species_name(s2_record['species'])

            out_handle.write('{0}-{1} {2} {3} {4}-{5} {6} {7}\n'.format(
                s1_name,
                s1_record['location']['contig'],
                s1_record['location']['start'],
                s1_record['location']['end'],
                s2_name,
                s2_record['location']['contig'],
                s2_record['location']['start'],
                s2_record['location']['end'],
                )
            )


def get_conf_file(links, name='circos', gc=None,):
    karyotypes_dir = os.path.join(OUTPUT, 'circos', 'karyotypes')
    karyotypes = [os.path.join(karyotypes_dir, x) for x in os.listdir(karyotypes_dir)]
    outdir = os.path.join(OUTPUT, 'circos', 'configuration_files')
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    outfile = os.path.join(outdir, '{}.conf'.format(name))

    with open(outfile, 'w+') as out_handle:
        out_handle.write("karyotype = {}".format(';'.join([f for f in karyotypes])))
        out_handle.write("""

chromosome_units = 10000

<ideogram>
<spacing>
default = 0.001r
</spacing>

radius = 0.8r
thickness = 40p
fill = yes
stroke_color = dgrey
stroke_thickness = 2p

</ideogram>
""")
        out_handle.write("""
<links>

<link>
file          = {}
color         = dgrey
radius        = 0.95r
bezier_radius = 0.1r
thickness     = 1
</link>

</links>
""".format(links))

        if gc:
            out_handle.write("<<include {}>>\n".format(gc))

        out_handle.write("<image>\n<<include {}>>\n</image>\n".format(os.path.join(CIRCOS, 'current', 'etc', 'image.conf')))
        out_handle.write("<<include {}>>\n".format(os.path.join(CIRCOS, 'current', 'etc', 'colors_fonts_patterns.conf')))
        out_handle.write("<<include {}>>\n".format(os.path.join(CIRCOS, 'current', 'etc', 'housekeeping.conf')))


def get_gc():
    for contig in db['genes'].find({'type': 'contig'}):
        gc_points = []
        seq = contig['dna_seq']

        for p in range(len(seq))[500::1000]:
            gc_cont = SeqUtils.GC(seq[p-500:p+499])
            gc_points.append((p-500, p+499, gc_cont))
        if gc_points:
            yield safe_species_name(contig['species']), contig['contig_id'], gc_points


def get_gc_conf(outfile = None):
    outdir = os.path.join(OUTPUT, 'circos', 'GC')
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    if not outfile:
        outfile = os.path.join(outdir, 'gc_plots.conf')

    with open(outfile, 'w+') as out_handle:
        out_handle.write("<plots>\n\n")
        for species, contig, gc_points in get_gc():
            points_file = get_gc_points_file(species, contig, gc_points)
            gc_values = [x[2] for x in gc_points]
            stats = (min(gc_values), max(gc_values), np.average(gc_values), np.std(gc_values))
            out_handle.write("""    <plot>
    show  = yes
    type  = line

    file  = {}
    r1    = 0.95r
    r0    = 1.05r
    max   = {}
    min   = {}

    color     = grey
    thickness = 1

    <rules>
    <rule>
    condition    = var(value) > {}
    color = dgreen
    </rule>
    <rule>
    condition    = var(value) < {}
    color = dred
    </rule>
    </rules>
    </plot>\n
    """.format(points_file, stats[1], stats[0], stats[2]+stats[3], stats[2]-stats[3])
                )
        out_handle.write('</plots>\n')


def get_gc_points_file(species, contig, gc_points):
    outdir = os.path.join(OUTPUT, 'circos', 'GC')
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    contig_name = "{}-{}".format(species, contig)

    with open(os.path.join(OUTPUT, 'circos', 'GC', "{}_gc.text".format(contig_name)), 'w+') as out_handle:
        for point in gc_points:
            out_handle.write("{} {} {} {}\n".format(
                contig_name,
                point[0],  # start
                point[1],  # end
                point[2],  # % GC
            ))

        return out_handle.name