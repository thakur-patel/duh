import smartpy as sp

FA2 = sp.import_script_from_url("https://smartpy.io/dev/templates/FA2.py")

class Cryptobot(FA2.FA2):

    @sp.entry_point
    def mint(self, params):
        sp.verify(sp.sender == self.data.administrator)
        
        if self.config.non_fungible:
            sp.verify(params.amount == 1, "NFT-asset: amount <> 1")
            sp.verify(~ self.token_id_set.contains(self.data.all_tokens, params.token_id), "NFT-asset: cannon mint the same token twice")
        
        user = self.ledger_key.make(params.address, params.token_id)
        self.token_id_set.add(self.data.all_tokens, params.token_id)
        sp.if self.data.ledger.contains(user):
            self.data.ledger[user].balance += params.amount
        sp.else:
            self.data.ledger[user] = FA2.Ledger_value.make(params.amount)
        
        sp.if self.data.tokens.contains(params.token_id):
            pass
        sp.else:
            self.data.tokens[params.token_id] = self.token_meta_data.make(
                amount = params.amount, 
                metadata = params.metadata
            )
        

@sp.add_test(name = "Cryptobot")
def test():
    scenario = sp.test_scenario()
    
    admin = sp.test_account("Admin")
    
    mark = sp.test_account("Mark")
    elon = sp.test_account("Mars")
    
    cryptobot = Cryptobot(FA2.FA2_config(non_fungible = True), admin = admin.address, metadata = sp.big_map({"": sp.bytes_of_string("tezos-storage:content"),"content": sp.bytes_of_string("""{"name" : "Cryptobot"}""")}))
    scenario += cryptobot
    
    
    scenario += cryptobot.mint(address = mark.address, 
                            amount = 1,
                            metadata= Cryptobot.make_metadata(
                                decimals = 0,
                                name = "Mark bot",
                                symbol = "CTB"
                            ),
                            token_id= 0
                            ).run(sender = admin)

    
    scenario += cryptobot.mint(address = elon.address,
                            amount = 1,
                            metadata = Cryptobot.make_metadata(
                                decimals = 0,
                                name = "Elon bot",
                                symbol = "CTB"
                            ),
                            token_id = 1).run(sender = admin)
                            
    # (1) Create a test account operator with the seed of "operator".              
    
    
    # (2) Call entry point update_operator and give operator the access to transfer token with token_id 0 for mark.
