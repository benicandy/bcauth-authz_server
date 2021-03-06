# 注意事項
# chaincodeのchannelを修正する
# package_idをOrg1とOrg2の分を修正する

# ネットワーク立ち上げ
cd ~/project-bcauth/fabric-samples/test-network;
./network.sh down;
# down から up までちょっと時間おいたほうがいいかも
./network.sh up createChannel;

# path を設定
export PATH=${PWD}/../bin:$PATH;
export FABRIC_CFG_PATH=$PWD/../config/;

# GO 関係の設定（意味は知らない）
cd ~/project-bcauth/fabric-samples/chaincode/uma/v2_timestamp/timestamp;
GO111MODULE=on go mod vendor;
cd ~/project-bcauth/fabric-samples/chaincode/uma/v2_timestamp/pat;
GO111MODULE=on go mod vendor;
cd ~/project-bcauth/fabric-samples/chaincode/uma/v2_timestamp/rreg;
GO111MODULE=on go mod vendor;
cd ~/project-bcauth/fabric-samples/chaincode/uma/v2_timestamp/policy;
GO111MODULE=on go mod vendor;
cd ~/project-bcauth/fabric-samples/chaincode/uma/v2_timestamp/perm;
GO111MODULE=on go mod vendor;
cd ~/project-bcauth/fabric-samples/chaincode/uma/v2_timestamp/token;
GO111MODULE=on go mod vendor;
cd ~/project-bcauth/fabric-samples/chaincode/uma/v2_timestamp/claim;
GO111MODULE=on go mod vendor;
cd ~/project-bcauth/fabric-samples/chaincode/uma/v2_timestamp/intro;
GO111MODULE=on go mod vendor;

# package
cd ~/project-bcauth/fabric-samples/test-network;
export PACKAGE_CC_NAME="timestamp";
peer lifecycle chaincode package $PACKAGE_CC_NAME.tar.gz --path ../chaincode/uma/v2_timestamp/$PACKAGE_CC_NAME/ --lang golang --label ${PACKAGE_CC_NAME}_1.0;
export PACKAGE_CC_NAME="pat";
peer lifecycle chaincode package $PACKAGE_CC_NAME.tar.gz --path ../chaincode/uma/v2_timestamp/$PACKAGE_CC_NAME/ --lang golang --label ${PACKAGE_CC_NAME}_1.0;
export PACKAGE_CC_NAME="rreg";
peer lifecycle chaincode package $PACKAGE_CC_NAME.tar.gz --path ../chaincode/uma/v2_timestamp/$PACKAGE_CC_NAME/ --lang golang --label ${PACKAGE_CC_NAME}_1.0;
export PACKAGE_CC_NAME="policy";
peer lifecycle chaincode package $PACKAGE_CC_NAME.tar.gz --path ../chaincode/uma/v2_timestamp/$PACKAGE_CC_NAME/ --lang golang --label ${PACKAGE_CC_NAME}_1.0;
export PACKAGE_CC_NAME="perm";
peer lifecycle chaincode package $PACKAGE_CC_NAME.tar.gz --path ../chaincode/uma/v2_timestamp/$PACKAGE_CC_NAME/ --lang golang --label ${PACKAGE_CC_NAME}_1.0;
export PACKAGE_CC_NAME="token";
peer lifecycle chaincode package $PACKAGE_CC_NAME.tar.gz --path ../chaincode/uma/v2_timestamp/$PACKAGE_CC_NAME/ --lang golang --label ${PACKAGE_CC_NAME}_1.0;
export PACKAGE_CC_NAME="claim";
peer lifecycle chaincode package $PACKAGE_CC_NAME.tar.gz --path ../chaincode/uma/v2_timestamp/$PACKAGE_CC_NAME/ --lang golang --label ${PACKAGE_CC_NAME}_1.0;
export PACKAGE_CC_NAME="intro";
peer lifecycle chaincode package $PACKAGE_CC_NAME.tar.gz --path ../chaincode/uma/v2_timestamp/$PACKAGE_CC_NAME/ --lang golang --label ${PACKAGE_CC_NAME}_1.0;

# コマンド操作を Org1MSP に設定
export CORE_PEER_TLS_ENABLED=true;
export CORE_PEER_LOCALMSPID="Org1MSP";
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt;
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp;
export CORE_PEER_ADDRESS=localhost:7051;

# instgall (Org1MSP)
cd ~/project-bcauth/fabric-samples/test-network;
export INSTALL_CC_NAME="timestamp";
peer lifecycle chaincode install $INSTALL_CC_NAME.tar.gz;
export INSTALL_CC_NAME="pat";
peer lifecycle chaincode install $INSTALL_CC_NAME.tar.gz;
export INSTALL_CC_NAME="rreg";
peer lifecycle chaincode install $INSTALL_CC_NAME.tar.gz;
export INSTALL_CC_NAME="policy";
peer lifecycle chaincode install $INSTALL_CC_NAME.tar.gz;
export INSTALL_CC_NAME="perm";
peer lifecycle chaincode install $INSTALL_CC_NAME.tar.gz;
export INSTALL_CC_NAME="token";
peer lifecycle chaincode install $INSTALL_CC_NAME.tar.gz;
export INSTALL_CC_NAME="claim";
peer lifecycle chaincode install $INSTALL_CC_NAME.tar.gz;
export INSTALL_CC_NAME="intro";
peer lifecycle chaincode install $INSTALL_CC_NAME.tar.gz;

# コマンド操作を Org2MSP に設定
export CORE_PEER_LOCALMSPID="Org2MSP";
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt;
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org2.example.com/users/Admin@org2.example.com/msp;
export CORE_PEER_ADDRESS=localhost:9051;

# install (Org2MSP)
export INSTALL_CC_NAME="timestamp";
peer lifecycle chaincode install $INSTALL_CC_NAME.tar.gz;
export INSTALL_CC_NAME="pat";
peer lifecycle chaincode install $INSTALL_CC_NAME.tar.gz;
export INSTALL_CC_NAME="rreg";
peer lifecycle chaincode install $INSTALL_CC_NAME.tar.gz;
export INSTALL_CC_NAME="policy";
peer lifecycle chaincode install $INSTALL_CC_NAME.tar.gz;
export INSTALL_CC_NAME="perm";
peer lifecycle chaincode install $INSTALL_CC_NAME.tar.gz;
export INSTALL_CC_NAME="token";
peer lifecycle chaincode install $INSTALL_CC_NAME.tar.gz;
export INSTALL_CC_NAME="claim";
peer lifecycle chaincode install $INSTALL_CC_NAME.tar.gz;
export INSTALL_CC_NAME="intro";
peer lifecycle chaincode install $INSTALL_CC_NAME.tar.gz;

# queryinstalled - package_id を確認
peer lifecycle chaincode queryinstalled;

# package_id を設定
# export CC_PACKAGE_NAME="timestamp";
# export CC_PACKAGE_ID=timestamp_1.0:da2a501329d0c438397d8e6afdd8c3083d9f51db796dad48b979d9849e74e46b;

# approveformyorg (Org2MSP)
export CC_PACKAGE_NAME="timestamp";
export CC_PACKAGE_ID=timestamp_1.0:c6c6f738635d7b373d58ff0431ee266af9c54af61b9abd5b882230d42d70ac25;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;
export CC_PACKAGE_NAME="pat";
export CC_PACKAGE_ID=pat_1.0:481bfe4fad1e33e54cd97cc5ff24526bd8d0ebd02365c37d337580c0dcdb28ed;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;
export CC_PACKAGE_NAME="rreg";
export CC_PACKAGE_ID=rreg_1.0:b2654a24039036b0b9caa1373f471a89101903b6987dd92f2a67222b49406eb5;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;
export CC_PACKAGE_NAME="policy";
export CC_PACKAGE_ID=policy_1.0:8be6bbe519998f5b4e6e64ad8df1c08d5eeead7f6b6cd126c4c011656b6e2384;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;
export CC_PACKAGE_NAME="perm";
export CC_PACKAGE_ID=perm_1.0:2fda651b8521e6aa6b97681cd406d654ce018bf4c3edad480a6dd79ce613e6c0;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;
export CC_PACKAGE_NAME="token";
export CC_PACKAGE_ID=token_1.0:c318bb01a3d72e8d445a0623b31f94b99341f0d3fbbe31f6712e5a9f23e0b0a8;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;
export CC_PACKAGE_NAME="claim";
export CC_PACKAGE_ID=claim_1.0:1bb6d06f9b16e3d3b38a4a595bde8dae275a28d2b592478b84b716c179502ef2;
export CC_PACKAGE_ID=claim_1.0:1bb6d06f9b16e3d3b38a4a595bde8dae275a28d2b592478b84b716c179502ef2;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;
export CC_PACKAGE_NAME="intro";
export CC_PACKAGE_ID=intro_1.0:b194a401988b87d7f5dba803021779948b22785d3da3167482e2a5f3b8916ae6;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;

# コマンド操作を Org1MSP に設定
export CORE_PEER_LOCALMSPID="Org1MSP";
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp;
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt;
export CORE_PEER_ADDRESS=localhost:7051;

# approveformyorg (Org1MSP)
export CC_PACKAGE_NAME="timestamp";
export CC_PACKAGE_ID=timestamp_1.0:c6c6f738635d7b373d58ff0431ee266af9c54af61b9abd5b882230d42d70ac25;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;
export CC_PACKAGE_NAME="pat";
export CC_PACKAGE_ID=pat_1.0:481bfe4fad1e33e54cd97cc5ff24526bd8d0ebd02365c37d337580c0dcdb28ed;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;
export CC_PACKAGE_NAME="rreg";
export CC_PACKAGE_ID=rreg_1.0:b2654a24039036b0b9caa1373f471a89101903b6987dd92f2a67222b49406eb5;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;
export CC_PACKAGE_NAME="policy";
export CC_PACKAGE_ID=policy_1.0:8be6bbe519998f5b4e6e64ad8df1c08d5eeead7f6b6cd126c4c011656b6e2384;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;
export CC_PACKAGE_NAME="perm";
export CC_PACKAGE_ID=perm_1.0:2fda651b8521e6aa6b97681cd406d654ce018bf4c3edad480a6dd79ce613e6c0;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;
export CC_PACKAGE_NAME="token";
export CC_PACKAGE_ID=token_1.0:c318bb01a3d72e8d445a0623b31f94b99341f0d3fbbe31f6712e5a9f23e0b0a8;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;
export CC_PACKAGE_NAME="claim";
export CC_PACKAGE_ID=claim_1.0:1bb6d06f9b16e3d3b38a4a595bde8dae275a28d2b592478b84b716c179502ef2;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;
export CC_PACKAGE_NAME="intro";
export CC_PACKAGE_ID=intro_1.0:b194a401988b87d7f5dba803021779948b22785d3da3167482e2a5f3b8916ae6;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;

# checkcommitreadiness - チャネルメンバーの approve 状況を確認できる．
peer lifecycle chaincode checkcommitreadiness --channelID mychannel --name intro --version 1.0 --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem --output json;

# commit
export COMMIT_CC_NAME="timestamp";
peer lifecycle chaincode commit -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $COMMIT_CC_NAME --version 1.0 --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt;
export COMMIT_CC_NAME="pat";
peer lifecycle chaincode commit -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $COMMIT_CC_NAME --version 1.0 --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt;
export COMMIT_CC_NAME="rreg";
peer lifecycle chaincode commit -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $COMMIT_CC_NAME --version 1.0 --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt;
export COMMIT_CC_NAME="policy";
peer lifecycle chaincode commit -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $COMMIT_CC_NAME --version 1.0 --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt;
export COMMIT_CC_NAME="perm";
peer lifecycle chaincode commit -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $COMMIT_CC_NAME --version 1.0 --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt;
export COMMIT_CC_NAME="token";
peer lifecycle chaincode commit -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $COMMIT_CC_NAME --version 1.0 --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt;
export COMMIT_CC_NAME="claim";
peer lifecycle chaincode commit -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $COMMIT_CC_NAME --version 1.0 --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt;
export COMMIT_CC_NAME="intro";
peer lifecycle chaincode commit -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $COMMIT_CC_NAME --version 1.0 --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt;

# queryinstalled
peer lifecycle chaincode querycommitted --channelID mychannel --name timestamp --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;

# ***** デバッグ用 **************************************************
# invoke（連続して実行するとエラー発生するので，時間をおいて実行する）
# timestamp
export INVOKE_CC_NAME="timestamp";
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n $INVOKE_CC_NAME --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"function":"checkTimestamp","Args":["1595230979","vF9Oyfm+G9qS4/Qfns5MgSZNYjOPlAIZVECh2I5Z7HHgdloy5q7gJoxi7c1S2/ebIQbEMLS05x3+b0WD0VJfcWSUwZMHr3jfXYYwbeZ1TerKpvfp1j21nZ+OEP26bc28rLRAYZsVQ4Ilx7qp+uLfxu9X9x37Qj3n0CI2TEiKYSSYDQ0bftQ/3iWSSoGjsDljh9bKz1eVL911KeUGO+t/9IkB6LtZghdbIlnGISbgrVGoEOtGHi0t8uD2Vh/CRyBe+XnQV3HQtkjddLQitAesKTYunK1Ctia3x7klVjRH9XiJ11q6IbR8gz7rchdHYZe6HP+w/LyWMS5z6M26AXQrVw=="]}';

sleep 3

# pat
export INVOKE_CC_NAME="pat";
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n $INVOKE_CC_NAME --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"function":"invoke","Args":["ro01","rs","1595230979","vF9Oyfm+G9qS4/Qfns5MgSZNYjOPlAIZVECh2I5Z7HHgdloy5q7gJoxi7c1S2/ebIQbEMLS05x3+b0WD0VJfcWSUwZMHr3jfXYYwbeZ1TerKpvfp1j21nZ+OEP26bc28rLRAYZsVQ4Ilx7qp+uLfxu9X9x37Qj3n0CI2TEiKYSSYDQ0bftQ/3iWSSoGjsDljh9bKz1eVL911KeUGO+t/9IkB6LtZghdbIlnGISbgrVGoEOtGHi0t8uD2Vh/CRyBe+XnQV3HQtkjddLQitAesKTYunK1Ctia3x7klVjRH9XiJ11q6IbR8gz7rchdHYZe6HP+w/LyWMS5z6M26AXQrVw=="]}';

sleep 3

# rreg - create
export INVOKE_CC_NAME="rreg";
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n $INVOKE_CC_NAME --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"function":"invoke","Args":["0xddb5ab8c5405830359d2af4ec8d4bdf27bc4b8ee7d20f64ec1a71a634e551","read:write","description","iconuri","name","type","1595230979","vF9Oyfm+G9qS4/Qfns5MgSZNYjOPlAIZVECh2I5Z7HHgdloy5q7gJoxi7c1S2/ebIQbEMLS05x3+b0WD0VJfcWSUwZMHr3jfXYYwbeZ1TerKpvfp1j21nZ+OEP26bc28rLRAYZsVQ4Ilx7qp+uLfxu9X9x37Qj3n0CI2TEiKYSSYDQ0bftQ/3iWSSoGjsDljh9bKz1eVL911KeUGO+t/9IkB6LtZghdbIlnGISbgrVGoEOtGHi0t8uD2Vh/CRyBe+XnQV3HQtkjddLQitAesKTYunK1Ctia3x7klVjRH9XiJ11q6IbR8gz7rchdHYZe6HP+w/LyWMS5z6M26AXQrVw=="]}';

sleep 3

# rreg - list
export INVOKE_CC_NAME="rreg";
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n $INVOKE_CC_NAME --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"function":"list","Args":["0xddb5ab8c5405830359d2af4ec8d4bdf27bc4b8ee7d20f64ec1a71a634e551"]}';

sleep 3

# rreg - query
export INVOKE_CC_NAME="rreg";
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n $INVOKE_CC_NAME --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"function":"query","Args":["0xddb5ab8c5405830359d2af4ec8d4bdf27bc4b8ee7d20f64ec1a71a634e551","08db20ba-2666-5b91-9bef-3d5b7d9138ae"]}';

sleep 3

# policy - invoke
export INVOKE_CC_NAME="policy";
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n $INVOKE_CC_NAME --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"function":"invoke","Args":["08db20ba-2666-5b91-9bef-3d5b7d9138ae","http://tff-01.ctiport.net:8888/authen","rqp_id","client_id"]}';

sleep 3

# policy - query
export INVOKE_CC_NAME="policy";
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n $INVOKE_CC_NAME --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"function":"query","Args":["08db20ba-2666-5b91-9bef-3d5b7d9138ae"]}';

sleep 3

# perm
export INVOKE_CC_NAME="perm";
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n $INVOKE_CC_NAME --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"function":"invoke","Args":["0xddb5ab8c5405830359d2af4ec8d4bdf27bc4b8ee7d20f64ec1a71a634e551","{{08db20ba-2666-5b91-9bef-3d5b7d9138ae,\"read\"}}","1595230979","vF9Oyfm+G9qS4/Qfns5MgSZNYjOPlAIZVECh2I5Z7HHgdloy5q7gJoxi7c1S2/ebIQbEMLS05x3+b0WD0VJfcWSUwZMHr3jfXYYwbeZ1TerKpvfp1j21nZ+OEP26bc28rLRAYZsVQ4Ilx7qp+uLfxu9X9x37Qj3n0CI2TEiKYSSYDQ0bftQ/3iWSSoGjsDljh9bKz1eVL911KeUGO+t/9IkB6LtZghdbIlnGISbgrVGoEOtGHi0t8uD2Vh/CRyBe+XnQV3HQtkjddLQitAesKTYunK1Ctia3x7klVjRH9XiJ11q6IbR8gz7rchdHYZe6HP+w/LyWMS5z6M26AXQrVw=="]}';

sleep 3

# token (claim_token なし)
export INVOKE_CC_NAME="token";
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n $INVOKE_CC_NAME --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"function":"invoke","Args":["urn:ietf:params:oauth:grant-type:uma-ticket","08db20ba-2666-5b91-9bef-3d5b7d9138ae","","","1595230979","vF9Oyfm+G9qS4/Qfns5MgSZNYjOPlAIZVECh2I5Z7HHgdloy5q7gJoxi7c1S2/ebIQbEMLS05x3+b0WD0VJfcWSUwZMHr3jfXYYwbeZ1TerKpvfp1j21nZ+OEP26bc28rLRAYZsVQ4Ilx7qp+uLfxu9X9x37Qj3n0CI2TEiKYSSYDQ0bftQ/3iWSSoGjsDljh9bKz1eVL911KeUGO+t/9IkB6LtZghdbIlnGISbgrVGoEOtGHi0t8uD2Vh/CRyBe+XnQV3HQtkjddLQitAesKTYunK1Ctia3x7klVjRH9XiJ11q6IbR8gz7rchdHYZe6HP+w/LyWMS5z6M26AXQrVw=="]}';

sleep 3

# claim
export INVOKE_CC_NAME="claim";
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n $INVOKE_CC_NAME --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"function":"invoke","Args":["client_id","76521234-8a03-53b2-aa5f-f73647ae86ce","http://tff-02.ctiport.net:8888/redirect-claims","1595230979","vF9Oyfm+G9qS4/Qfns5MgSZNYjOPlAIZVECh2I5Z7HHgdloy5q7gJoxi7c1S2/ebIQbEMLS05x3+b0WD0VJfcWSUwZMHr3jfXYYwbeZ1TerKpvfp1j21nZ+OEP26bc28rLRAYZsVQ4Ilx7qp+uLfxu9X9x37Qj3n0CI2TEiKYSSYDQ0bftQ/3iWSSoGjsDljh9bKz1eVL911KeUGO+t/9IkB6LtZghdbIlnGISbgrVGoEOtGHi0t8uD2Vh/CRyBe+XnQV3HQtkjddLQitAesKTYunK1Ctia3x7klVjRH9XiJ11q6IbR8gz7rchdHYZe6HP+w/LyWMS5z6M26AXQrVw=="]}';

sleep 3

# token (claim_token あり)
export INVOKE_CC_NAME="token";
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n $INVOKE_CC_NAME --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"function":"invoke","Args":["urn:ietf:params:oauth:grant-type:uma-ticket","cc1954ea-f8f4-58f4-b05c-c9c19f6162cf","{\"iss\":http://tff-01.ctiport.net:8888/authen,\"sub\":rqp_id,\"aud\":client_id}","http://openid.net/specs/openid-connect-core-1_0.html#IDToken","1595230979","vF9Oyfm+G9qS4/Qfns5MgSZNYjOPlAIZVECh2I5Z7HHgdloy5q7gJoxi7c1S2/ebIQbEMLS05x3+b0WD0VJfcWSUwZMHr3jfXYYwbeZ1TerKpvfp1j21nZ+OEP26bc28rLRAYZsVQ4Ilx7qp+uLfxu9X9x37Qj3n0CI2TEiKYSSYDQ0bftQ/3iWSSoGjsDljh9bKz1eVL911KeUGO+t/9IkB6LtZghdbIlnGISbgrVGoEOtGHi0t8uD2Vh/CRyBe+XnQV3HQtkjddLQitAesKTYunK1Ctia3x7klVjRH9XiJ11q6IbR8gz7rchdHYZe6HP+w/LyWMS5z6M26AXQrVw=="]}';

sleep 3

# intro
export INVOKE_CC_NAME="intro";
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n $INVOKE_CC_NAME --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"function":"invoke","Args":["0xddb5ab8c5405830359d2af4ec8d4bdf27bc4b8ee7d20f64ec1a71a634e551","fee1ed43-99b3-526e-850f-b66333d9dcbb"]}';



export PATH=${PWD}/../bin:$PATH; export FABRIC_CFG_PATH=$PWD/../config/; export CORE_PEER_TLS_ENABLED=true; export CORE_PEER_LOCALMSPID="Org1MSP"; export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt; export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp; export CORE_PEER_ADDRESS=localhost:7051; export INVOKE_CC_NAME="perm";
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n $INVOKE_CC_NAME --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"function":"invoke","Args":["{{0xddb5ab8c5405830359d2af4ec8d4bdf27bc4b8ee7d20f64ec1a71a634e551,08db20ba-2666-5b91-9bef-3d5b7d9138ae,\"tff\"},{0x23e6958b1f555b905ade2f915c8c64453bd9514c4e1750d995f17215cbc4,1c1f1d9f-051c-592f-bb06-5ec8cef664ba,\"tff:read\"}}","1595230979","vF9Oyfm+G9qS4/Qfns5MgSZNYjOPlAIZVECh2I5Z7HHgdloy5q7gJoxi7c1S2/ebIQbEMLS05x3+b0WD0VJfcWSUwZMHr3jfXYYwbeZ1TerKpvfp1j21nZ+OEP26bc28rLRAYZsVQ4Ilx7qp+uLfxu9X9x37Qj3n0CI2TEiKYSSYDQ0bftQ/3iWSSoGjsDljh9bKz1eVL911KeUGO+t/9IkB6LtZghdbIlnGISbgrVGoEOtGHi0t8uD2Vh/CRyBe+XnQV3HQtkjddLQitAesKTYunK1Ctia3x7klVjRH9XiJ11q6IbR8gz7rchdHYZe6HP+w/LyWMS5z6M26AXQrVw=="]}';


# <Chaincode 修正用>
export PACKAGE_CC_NAME="perm";
export INSTALL_CC_NAME="perm";

cd ~/project-bcauth/fabric-samples/test-network;
./network.sh down;
# ↑から↓までちょっと時間おいたほうがいいかも
./network.sh up createChannel;

# path を設定
export PATH=${PWD}/../bin:$PATH;
export FABRIC_CFG_PATH=$PWD/../config/;

# GO 関係の設定（意味は知らない）
cd ~/project-bcauth/fabric-samples/chaincode/uma/v2_timestamp/perm;
GO111MODULE=on go mod vendor;


# package
cd ~/project-bcauth/fabric-samples/test-network;
peer lifecycle chaincode package $PACKAGE_CC_NAME.tar.gz --path ../chaincode/uma/v2_timestamp/$PACKAGE_CC_NAME/ --lang golang --label ${PACKAGE_CC_NAME}_1.0;

# コマンド操作を Org1MSP に設定
export CORE_PEER_TLS_ENABLED=true;
export CORE_PEER_LOCALMSPID="Org1MSP";
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt;
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp;
export CORE_PEER_ADDRESS=localhost:7051;

# instgall (Org1MSP)
cd ~/project-bcauth/fabric-samples/test-network;
peer lifecycle chaincode install $INSTALL_CC_NAME.tar.gz;



# rreg - update
export INVOKE_CC_NAME="rreg";
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n $INVOKE_CC_NAME --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"function":"update","Args":["0xddb5ab8c5405830359d2af4ec8d4bdf27bc4b8ee7d20f64ec1a71a634e551","08db20ba-2666-5b91-9bef-3d5b7d9138ae","tff","sample_dataset","","20201220_171418_example.txt",""]}';
