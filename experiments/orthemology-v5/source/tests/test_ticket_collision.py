import unittest
from unittest.mock import patch
from operational import Engine
from boundaries import Rejection

class TicketCollisionTests(unittest.TestCase):
 def test_collision_cannot_replace_an_existing_ticket_record(self):
  e=Engine.standard()
  with patch('operational.secrets.token_hex',return_value='a'*48):
   old=e.admit({'op':'primitive','name':'succ'})
   self.assertEqual(e.dispatch(old,4),5)
   with self.assertRaises(Rejection):e.admit({'op':'primitive','name':'iszero'})
   self.assertEqual(e.dispatch(old,4),5)
 def test_collision_cannot_revive_revoked_ticket(self):
  e=Engine.standard()
  with patch('operational.secrets.token_hex',return_value='b'*48):
   old=e.admit({'op':'primitive','name':'succ'});e.revise_rule('primitive:succ',False)
   with self.assertRaises(Rejection):e.admit({'op':'primitive','name':'iszero'})
   with self.assertRaises(Rejection):e.dispatch(old,0)

class IssuerBindingTests(unittest.TestCase):
 def test_identical_ticket_bytes_in_two_engines_do_not_cross_authorise(self):
  a,b=Engine.standard(),Engine.standard()
  with patch('operational.secrets.token_hex',return_value='c'*48):
   la=a.admit({'op':'primitive','name':'succ'});lb=b.admit({'op':'primitive','name':'iszero'})
  self.assertEqual(la.ticket,lb.ticket)
  self.assertEqual(a.dispatch(la,0),1);self.assertIs(b.dispatch(lb,0),True)
  with self.assertRaises(Rejection):b.dispatch(la,0)
  with self.assertRaises(Rejection):a.dispatch(lb,0)
