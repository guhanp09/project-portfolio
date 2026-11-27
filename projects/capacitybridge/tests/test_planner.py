import unittest
from dataclasses import replace

from capacitybridge.planner import Asset, eligible, make_inputs, solve, operating_cost, validate_inputs


class PlanningTests(unittest.TestCase):
    def small(self):
        a=Asset("A","city","PM",internal_cap=2,external_cap=3,
                min_heads=(1,1,1),max_heads=(1,1,1))
        return a,{("city","PM","D0"):3,("city","PM","regular"):2}

    def test_d0_cutoff(self):
        self.assertTrue(eligible("AM","D0","3pl"))
        self.assertFalse(eligible("PM","D0","3pl"))
        self.assertTrue(eligible("PM","D0","internal"))
        self.assertTrue(eligible("PM","regular","3pl"))

    def test_small_capacity_and_deadline(self):
        a,d=self.small();s=solve([a],d)
        self.assertEqual(s["missed","city","PM","D0"],1)
        self.assertEqual(s["flow","A","PM","D0","internal"],2)
        self.assertEqual(s["flow","A","PM","regular","3pl"],2)
        self.assertNotIn(("flow","A","PM","D0","3pl"),s)

    def test_hand_calculated_cost(self):
        a,d=self.small();s=solve([a],d);cost=operating_cost([a],s)
        self.assertEqual(cost["staff_cost_inr"],4*(135+130+115))
        self.assertEqual(cost["reservation_cost_inr"],4*2)
        self.assertEqual(cost["delivery_cost_inr"],2*18+2*30)
        self.assertEqual(cost["operating_cost_inr"],1624)

    def test_frozen_capacity_cannot_see_actual_demand(self):
        a,d=self.small();plan=solve([a],d);copy=plan.copy()
        actual={k:100 for k in d};r=solve([a],actual,frozen=plan)
        self.assertEqual(plan,copy)
        self.assertEqual(sum(v for k,v in r.items() if k[0]=="flow"),4)

    def test_zero_supply_stays_visible_as_missed(self):
        a,d=self.small();a=replace(a,internal_cap=0,external_cap=0,min_heads=(0,0,0),max_heads=(0,0,0))
        s=solve([a],d)
        self.assertEqual(sum(v for k,v in s.items() if k[0]=="missed"),5)

    def test_zero_demand(self):
        a,d=self.small();s=solve([a],{k:0 for k in d})
        self.assertEqual(sum(v for k,v in s.items() if k[0]=="flow"),0)

    def test_integer_and_conservation(self):
        assets,d=make_inputs("peak");s=solve(assets,d)
        self.assertTrue(all(v>=0 and int(v)==v for v in s.values()))
        for (city,wave,promise),amount in d.items():
            delivered=sum(v for k,v in s.items() if k[0]=="flow" and k[2:4]==(wave,promise)
                          and any(a.fc==k[1] and a.city==city for a in assets))
            self.assertEqual(delivered+s["missed",city,wave,promise],amount)

    def test_total_carrier_outage(self):
        a,d=self.small();plan=solve([a],d)
        r=solve([a],d,frozen=plan,internal_factor=0)
        self.assertEqual(r["missed","city","PM","D0"],3)

    def test_packing_outage(self):
        a,d=self.small();plan=solve([a],d)
        r=solve([a],d,frozen=plan,packing_factor=0)
        self.assertEqual(sum(v for k,v in r.items() if k[0]=="missed"),5)

    def test_duplicate_assets_rejected(self):
        a,d=self.small()
        with self.assertRaises(ValueError):solve([a,a],d)

    def test_missing_demand_key_rejected(self):
        a,d=self.small();d.pop(("city","PM","D0"))
        with self.assertRaises(ValueError):solve([a],d)

    def test_negative_or_fractional_demand_rejected(self):
        a,d=self.small()
        for bad in (-1,.5,float("nan")):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):validate_inputs([a],{k:bad for k in d})

    def test_invalid_availability_rejected(self):
        a,d=self.small()
        with self.assertRaises(ValueError):solve([a],d,packing_factor=-.1)


if __name__ == "__main__":unittest.main()
