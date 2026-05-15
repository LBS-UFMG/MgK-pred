import os
from Bio.PDB import PDBParser, MMCIFParser, NeighborSearch, MMCIFIO, Select

# Diretórios
input_dir = "pdbs"
output_dir = "ions"
os.makedirs(output_dir, exist_ok=True)

# Distância cutoff
CUTOFF = 6.0

# Aminoácidos padrão
AMINO_ACIDS = {
    "ALA","ARG","ASN","ASP","CYS","GLU","GLN","GLY",
    "HIS","ILE","LEU","LYS","MET","PHE","PRO","SER",
    "THR","TRP","TYR","VAL"
}

# Parsers
pdb_parser = PDBParser(QUIET=True)
cif_parser = MMCIFParser(QUIET=True)

class AtomSelect(Select):
    def __init__(self, atoms_to_keep):
        self.atoms_to_keep = atoms_to_keep

    def accept_atom(self, atom):
        return atom in self.atoms_to_keep


for file in os.listdir(input_dir):

    if not (file.endswith(".pdb") or file.endswith(".cif") or file.endswith(".mmcif")):
        continue

    file_path = os.path.join(input_dir, file)
    pdb_id = os.path.splitext(file)[0]

    # Escolher parser automaticamente
    if file.endswith(".pdb"):
        structure = pdb_parser.get_structure(pdb_id, file_path)
    else:
        structure = cif_parser.get_structure(pdb_id, file_path)

    # Coletar todos os átomos
    all_atoms = list(structure.get_atoms())
    ns = NeighborSearch(all_atoms)

    for atom in all_atoms:
        element = atom.element.strip().upper()

        if element not in ["MG", "K"]:
            continue

        ion_name = element

        # mmCIF pode não ter serial confiável
        atom_serial = atom.get_serial_number() or id(atom)

        # Encontrar vizinhos
        neighbors = ns.search(atom.coord, CUTOFF)

        atoms_to_save = set()
        atoms_to_save.add(atom)

        for neigh in neighbors:
            res = neigh.get_parent()
            resname = res.get_resname().strip()

            # Se for aminoácido → pega TODOS os átomos do resíduo
            if resname in AMINO_ACIDS:
                for a in res.get_atoms():
                    atoms_to_save.add(a)
            else:
                atoms_to_save.add(neigh)

        # Salvar como mmCIF
        output_name = f"{pdb_id}_{ion_name}_{atom_serial}.cif"
        output_path = os.path.join(output_dir, output_name)

        io = MMCIFIO()
        io.set_structure(structure)
        io.save(output_path, AtomSelect(atoms_to_save))

print("Processamento concluído.")