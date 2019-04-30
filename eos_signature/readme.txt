## 1.创建合约账号
```
cleos system newaccount  --transfer eosio signature EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV --stake-net "100.0000 EOS" --stake-cpu "100.0000 EOS" --buy-ram "100.0000 EOS"
```

## 2.编译,部署智能合约

```
cd $HOME/wyl/work/tools/contracts/signature
eosiocpp -g signature.abi signature.cpp 
eosiocpp -o signature.wast signature.cpp 

cleos set contract signature ../signature/ -p signature

```

```
/*
第一个参数:对hello进行哈希
第二个参数:用5KBiNrdgkVfqnA3FH1eNjgK1uLBdswSJ7opgHPfT6YUn7SE3a9W私钥对hello签名
第三个参数:5KBiNrdgkVfqnA3FH1eNjgK1uLBdswSJ7opgHPfT6YUn7SE3a9W对应的公钥
*/
cleos push action signature keycheck '["2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824", "SIG_K1_K8QZmQMNJjwG8UYkzLUdgjsWC3V1jg8RNAm1ZrQy6TiTumZfwKMnE5Mg3zBUeCtwaTwEgTeNRkDGUfvtTuYXF5mULRmdxN", "EOS6JQynmnt7nGQJq6sTtWCtM5kAbK2Bx5fWCZwcSsSskfUvpRLDQ"]' -p signature

```


```
cleos push action signature hashcheck '["abcfe123fda452daf5325df3f1254f35fd1565d1312dfa3fd1f24fda45123129", "64153ec5eeb1f32f9e600212048d0c9037eca582fb2617ff2360e51419f94ac4"]' -p signature

cleos push action signature hashcheckv2 '["abcfe123fda452daf5325df3f1254f35fd1565d1312dfa3fd1f24fda45123129", "64153ec5eeb1f32f9e600212048d0c9037eca582fb2617ff2360e51419f94ac4"]' -p signature

```


