const ecc = require('eosjs-ecc')


ecc.randomKey().then(privateKey => {
    const data = "hello";
    const priKey = "5KBiNrdgkVfqnA3FH1eNjgK1uLBdswSJ7opgHPfT6YUn7SE3a9W";
    console.log('data:\t', data) // data
    console.log('Private Key:\t', priKey) // wif
    console.log('Public Key:\t', ecc.privateToPublic(priKey)) // EOSkey...
    const res = ecc.sign(data, priKey);

    console.log('===== res ====: ', res);
});


