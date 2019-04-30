#include <eosiolib/eosio.hpp>
#include <eosiolib/crypto.h>
#include <string>


template<typename CharT>
static std::string to_hex( const CharT* d, uint32_t s ) {
    std::string r;
    const char* to_hex="0123456789abcdef";
    uint8_t* c = (uint8_t*)d;
    for( uint32_t i = 0; i < s; ++i ) {
        (r += to_hex[(c[i] >> 4)]) += to_hex[(c[i] & 0x0f)];
    }
return r;
}

namespace example {

   using namespace eosio;

   class recover : public contract
   {
     public:
     using contract::contract;

     recover(account_name self) : contract(self) {};

     std::string sha256_to_hex(const checksum256& sha256) {
        return to_hex((char*)sha256.hash, sizeof(sha256.hash));
     }

    /*—È«©*/
    ///@abi action
    void keycheck(const checksum256 &digest, const signature &sig, const public_key &crosscheck_pk)
    {
        require_auth(_self);
        public_key pk;
        auto r = recover_key(&digest, (char *)&sig, sizeof(sig), (char *)&pk, sizeof(pk));
        print_f("public_key: %\n", to_hex(&pk, sizeof(pk)).c_str());
        print_f("crosscheck public_key: %\n", to_hex(&crosscheck_pk, sizeof(crosscheck_pk)).c_str());
        auto cmp = memcmp(&pk, &crosscheck_pk, sizeof(public_key));
        eosio_assert(memcmp(&pk, &crosscheck_pk, sizeof(public_key)) == 0, "keycheck: pubkey cross check failed");
    }

    ///@abi action
    void hashcheck(const std::string &data, const checksum256& hash)
    {
        print("begin.\n");
        assert_sha256(data.c_str(),
                      strlen(data.c_str()),
                      (const checksum256*)&hash);
        print("en.\n");
    }

    ///@abi action
    void hashcheckv2(const checksum256& data, const checksum256& hash)
    {
        print("begin...");
        print_f("data: %..", sha256_to_hex(data).c_str());
        std::string seed_str = sha256_to_hex(data);
        assert_sha256(seed_str.c_str(),
                      strlen(seed_str.c_str()),
                      (const checksum256*)&hash);
        print("en...");
    }

   };

}
EOSIO_ABI(example::recover, (keycheck)(hashcheck)(hashcheckv2))
