from collections import defaultdict

class CFGdenCNFyeDonusturucu:
    def __init__(self, gramer, baslangic_simgesi):
        self.gramer = gramer
        self.baslangic_simgesi = baslangic_simgesi
        self.sayac = 1
        self.yeni_deg_sonek = "X"
        self.cnf_gramer = defaultdict(list)

    def yeni_deg_uret(self):
        deg = f"{self.yeni_deg_sonek}{self.sayac}"
        self.sayac +=1
        return deg
        
    def bos_uretimleri_kaldir(self):
        nullable = set()
        degisti = True
        while degisti:
            degisti = False
            for sol in self.gramer:
                for uretim in self.gramer[sol]:
                    if uretim == ['ε'] or all(s in nullable for s in uretim):
                        if sol not in nullable:
                            nullable.add(sol)
                            degisti = True
        yeni_gramer = defaultdict(list)
        for sol in self.gramer:
            for uretim in self.gramer[sol]:
                if uretim == ['ε']:
                    continue
                indeksler = [i for i, s in enumerate(uretim) if s in nullable]
                for i in range(1 << len(indeksler)):
                    yeni_uretim = uretim[:]
                    for j, indeks in enumerate(indeksler):
                        if (i >> j) & 1:
                            yeni_uretim[indeks] = None
                    sonuc = [s for s in yeni_uretim if s is not None]
                    if not sonuc:
                        if sol == self.baslangic_simgesi and ['ε'] not in yeni_gramer[sol]:
                            yeni_gramer[sol].append(['ε'])
                    else:
                        if sonuc not in yeni_gramer[sol]:
                            yeni_gramer[sol].append(sonuc)
        for sol in list(yeni_gramer.keys()):
            if sol != self.baslangic_simgesi:
                yeni_gramer[sol] = [u for u in yeni_gramer[sol] if u != ['ε']]
        self.gramer = yeni_gramer
        self.nullable = nullable

    def birim_uretimleri_kaldir(self):
        birim_ciftler = set()
        for sol in self.gramer:
            for uretim in self.gramer[sol]:
                if len(uretim) == 1 and uretim[0].isupper() and uretim[0] != sol:
                    birim_ciftler.add((sol, uretim[0]))
        degisti = True
        while degisti:  
            degisti = False
            yeni_ciftler = set()
            for (A, B) in birim_ciftler:
                for (C, D) in birim_ciftler:
                    if B == C and (A, D) not in birim_ciftler and A != D:
                        yeni_ciftler.add((A,D))
                        degisti = True
            birim_ciftler |= yeni_ciftler

        yeni_gramer = defaultdict(list)
        for sol in self.gramer:
            for uretim in self.gramer[sol]:
                if not (len(uretim) == 1 and uretim[0].isupper()):
                    if uretim not in yeni_gramer[sol]:
                        yeni_gramer[sol].append(uretim)

        for (A, B) in birim_ciftler:
            if A == B:
                continue     #kendini üretmeyi engelle                   

            for uretim in self.gramer[B]:
                if len(uretim) == 1 and uretim[0].isupper():
                    continue
                if uretim not in yeni_gramer[A]:
                    yeni_gramer[A].append(uretim)

        #kendini üretim varsa cıkar
        for     sol in list(neyi for neyi in yeni_gramer.keys()):
            yeni_gramer[sol] = [u for u in yeni_gramer[sol] if not (len(u) == 1 and u[0] == sol)]

        self.gramer = yeni_gramer   

    def uzun_uretimlerdeki_terminalleri_degistir(self):
        terminal_harita = {}
        for sol in list(self.gramer.keys()):
            yeni_uretimler = []        
            for uretim in self.gramer[sol]:
                yeni_uretim = []
                for s in uretim:
                    if s.islower() and len(s) == 1:
                        if s not in terminal_harita:
                            yeni_deg = self.yeni_deg_uret()
                            terminal_harita[s] = yeni_deg
                            self.gramer[yeni_deg] = [[s]]
                        yeni_uretim.append(terminal_harita[s])
                    else:
                        yeni_uretim.append(s)
                yeni_uretimler.append(yeni_uretim)    
            self.gramer[sol] = yeni_uretimler

    def ikili_uretimlere_donustur(self):
        yeni_gramer = defaultdict(list)
        for sol in self.gramer:
            for uretim in self.gramer[sol]:
                while len(uretim) > 2:
                    yeni_deg = self.yeni_deg_uret()
                    ilk, ikinci = uretim[0], uretim[1]
                    yeni_gramer[yeni_deg].append([ilk,ikinci])
                    uretim = [yeni_deg] + uretim[2:]
                yeni_gramer[sol].append(uretim)
        self.gramer = yeni_gramer

    def baslangic_sembolunu_degistir(self):
        yeni_baslangic = self.baslangic_simgesi + "0"     
        if any(self.baslangic_simgesi in u for prod in self.gramer.values() for u in prod):
            self.gramer[yeni_baslangic] = [[self.baslangic_simgesi]]
            self.baslangic_simgesi = yeni_baslangic

    def kullanissiz_uretimleri_kaldir(self):
        generating = set()
        degisti = True
        while  degisti:     
            degisti = False
            for sol in self.gramer:
                for uretim in self.gramer[sol]:   
                    if all(s not in self.gramer or s in generating or not s.isupper() for s in uretim):
                        if sol not in generating:
                            generating.add(sol)
                            degisti = True
        yeni_gramer = defaultdict(list)
        for sol in self.gramer:
            if sol in generating:
                for uretim in self.gramer[sol]:
                    if all(s not in self.gramer or s in generating or not s.isupper() for s in uretim):
                        yeni_gramer[sol].append(uretim)
        self.gramer = yeni_gramer

        reachable = set([self.baslangic_simgesi])
        degisti = True
        while degisti:
            degisti = False
            for sol in list (reachable):
                for uretim in self.gramer.get(sol, []):
                    for s in uretim:
                        
                            if s in self.gramer and s not in reachable:
                                reachable.add(s)
                                degisti = True
        yeni_gramer2 = defaultdict(list)
        for sol in self.gramer:
            if sol in reachable:
                for uretim in self.gramer[sol]:
                    yeni_gramer2[sol].append(uretim)
        self.gramer = yeni_gramer2

    def cnfye_donustur(self):
        self.baslangic_sembolunu_degistir()
        self.bos_uretimleri_kaldir()
        self.birim_uretimleri_kaldir()
        self.kullanissiz_uretimleri_kaldir()
        self.uzun_uretimlerdeki_terminalleri_degistir()
        self.ikili_uretimlere_donustur()

        if hasattr(self, 'nullable') and self.baslangic_simgesi in self.nullable:
            if ['ε'] not in self.gramer[self.baslangic_simgesi]:
                self.gramer[self.baslangic_simgesi].append(['ε'])

        self.cnf_gramer = self.gramer
        return self.cnf_gramer

def grameri_yazdir(gramer):
    print("\nGramer:")
    for sol, uretimler in sorted(gramer.items()):
        for uretim in uretimler:
            print(f"{sol} -> {' '.join(uretim)}")

def main():
    ornek_gramerler = [
        {
            "gramer": {
                'S': [['A', 'B'], ['B', 'C'], ['ε'], ['C', 'C'], ['b'], ['a'], ['B', 'A']],
                'A': [['B', 'A'], ['a'], ['A']],  # 'A' -> 'A' kaldırılmalı dönüşümde
                'B': [['C', 'C'], ['b'], ['A', 'B'], ['a'], ['B', 'A']],
                'C': [['A', 'B'], ['a'], ['B', 'A']]
            },
            "baslangic": 'S'
        },
        {
            "gramer": {
                "S": [["A", "B"], ["b"]],
                "A": [["a"], ["S"]],
                "B": [["b"], ["A", "a"]],
            },
            "baslangic": 'S'
        },
        {
            "gramer": {
                "S": [["a"], ["a", "A"], ["B"]],
                "A": [["a", "B", "B"], ["ε"]],
                "B": [["A", "a"], ["b"]],
            },
            "baslangic": 'S'
        }
    ]

    for idx, ornek in enumerate(ornek_gramerler, 1):
        print(f"\n--- Örnek Gramer {idx} ---")
        donusturucu = CFGdenCNFyeDonusturucu(ornek["gramer"], ornek["baslangic"])
        cnf_gramer = donusturucu.cnfye_donustur()
        grameri_yazdir(cnf_gramer)

if __name__ == "__main__":
    main()
    