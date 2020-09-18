#     def get_playable_sets(self, set_size, set_num):
#         normal_cards = [c.rank for c in self.hand if not c.is_wildcard]
#         wildcards = [c.rank for c in self.hand if c.is_wildcard]
#         
#         normal_cards_counter = Counter(normal_cards)
#         wildcard_num = len(wildcards)
#         
#         sets_created = 0
#         sets_seen = {}
#         for i in range(set_size, set_size//2, -1):
#             jokers_needed = set_size - i
# #             print("{}/{} sets found so far. {} wildcards left.".format(sets_created, set_num, wildcard_num)) 
# #             print("Checking for sets of {}, {} wildcards needed.".format(i, jokers_needed)) 
#             
#             valid_sets = [c for c in normal_cards_counter if normal_cards_counter[c] >= i]
#             for s in valid_sets:
#                 if wildcard_num - jokers_needed >= 0:
#                     if s not in sets_seen:
#                         wildcard_num = wildcard_num - jokers_needed
#                         sets_created = sets_created + 1
#                         sets_seen[s] = jokers_needed
# #                         print(s, "with {} wildcards".format(jokers_needed))
#                     else:
# #                         print("We already used {}.".format(s))
#                         pass
#                 else:
# #                     print("Out of wildcards! Quitting search early.")
#                     break
#             if not valid_sets:
# #                 print("No sets of {} found.".format(i))
#                 pass
#     
# #         print("Found {}/{} valid sets with {} leftover wildcards".format(sets_created, set_num, wildcard_num))
#         
#         return sets_seen if len(sets_seen) >= set_num else None