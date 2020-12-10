# 注意事項
# chaincodeのchannelを修正する
# package_idをOrg1とOrg2の分を修正する

# ネットワーク立ち上げ
cd ~/project-bcauth/fabric-samples/test-network;
./network.sh down;
# ↑から↓までちょっと時間おいたほうがいいかも
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


# package
cd ~/project-bcauth/fabric-samples/test-network;
export PACKAGE_CC_NAME="timestamp";
peer lifecycle chaincode package $PACKAGE_CC_NAME.tar.gz --path ../chaincode/uma/v2_timestamp/$PACKAGE_CC_NAME/ --lang golang --label ${PACKAGE_CC_NAME}_1.0;
export PACKAGE_CC_NAME="pat";
peer lifecycle chaincode package $PACKAGE_CC_NAME.tar.gz --path ../chaincode/uma/v2_timestamp/$PACKAGE_CC_NAME/ --lang golang --label ${PACKAGE_CC_NAME}_1.0;
export PACKAGE_CC_NAME="rreg";
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

# queryinstalled - package_id を確認
peer lifecycle chaincode queryinstalled;

# package_id を設定
# export CC_PACKAGE_NAME="timestamp";
# export CC_PACKAGE_ID=timestamp_1.0:da2a501329d0c438397d8e6afdd8c3083d9f51db796dad48b979d9849e74e46b;

# approveformyorg (Org2MSP)
export CC_PACKAGE_NAME="timestamp";
export CC_PACKAGE_ID=timestamp_1.0:da2a501329d0c438397d8e6afdd8c3083d9f51db796dad48b979d9849e74e46b;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;
export CC_PACKAGE_NAME="pat";
export CC_PACKAGE_ID=pat_1.0:481bfe4fad1e33e54cd97cc5ff24526bd8d0ebd02365c37d337580c0dcdb28ed;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;
export CC_PACKAGE_NAME="rreg";
export CC_PACKAGE_ID=rreg_1.0:e56d22575b7d41c953a85fc013976b7a182117a0560c4e8bbbf8e538f03e4f07;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;


# コマンド操作を Org1MSP に設定
export CORE_PEER_LOCALMSPID="Org1MSP";
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp;
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt;
export CORE_PEER_ADDRESS=localhost:7051;

# approveformyorg (Org1MSP)
export CC_PACKAGE_NAME="timestamp";
export CC_PACKAGE_ID=timestamp_1.0:da2a501329d0c438397d8e6afdd8c3083d9f51db796dad48b979d9849e74e46b;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;
export CC_PACKAGE_NAME="pat";
export CC_PACKAGE_ID=pat_1.0:481bfe4fad1e33e54cd97cc5ff24526bd8d0ebd02365c37d337580c0dcdb28ed;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;
export CC_PACKAGE_NAME="rreg";
export CC_PACKAGE_ID=rreg_1.0:e56d22575b7d41c953a85fc013976b7a182117a0560c4e8bbbf8e538f03e4f07;
peer lifecycle chaincode approveformyorg -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $CC_PACKAGE_NAME --version 1.0 --package-id $CC_PACKAGE_ID --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem;

# commit
export COMMIT_CC_NAME="timestamp";
peer lifecycle chaincode commit -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $COMMIT_CC_NAME --version 1.0 --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt;
export COMMIT_CC_NAME="pat";
peer lifecycle chaincode commit -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $COMMIT_CC_NAME --version 1.0 --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt;
export COMMIT_CC_NAME="rreg";
peer lifecycle chaincode commit -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --channelID mychannel --name $COMMIT_CC_NAME --version 1.0 --sequence 1 --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt;

# invoke
# timestamp
export INVOKE_CC_NAME="timestamp";
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n $INVOKE_CC_NAME --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"function":"checkTimestamp","Args":["1595230979","vF9Oyfm+G9qS4/Qfns5MgSZNYjOPlAIZVECh2I5Z7HHgdloy5q7gJoxi7c1S2/ebIQbEMLS05x3+b0WD0VJfcWSUwZMHr3jfXYYwbeZ1TerKpvfp1j21nZ+OEP26bc28rLRAYZsVQ4Ilx7qp+uLfxu9X9x37Qj3n0CI2TEiKYSSYDQ0bftQ/3iWSSoGjsDljh9bKz1eVL911KeUGO+t/9IkB6LtZghdbIlnGISbgrVGoEOtGHi0t8uD2Vh/CRyBe+XnQV3HQtkjddLQitAesKTYunK1Ctia3x7klVjRH9XiJ11q6IbR8gz7rchdHYZe6HP+w/LyWMS5z6M26AXQrVw=="]}';

# pat - create
export INVOKE_CC_NAME="pat";
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n $INVOKE_CC_NAME --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"function":"invoke","Args":["ro","rs","1595230979","vF9Oyfm+G9qS4/Qfns5MgSZNYjOPlAIZVECh2I5Z7HHgdloy5q7gJoxi7c1S2/ebIQbEMLS05x3+b0WD0VJfcWSUwZMHr3jfXYYwbeZ1TerKpvfp1j21nZ+OEP26bc28rLRAYZsVQ4Ilx7qp+uLfxu9X9x37Qj3n0CI2TEiKYSSYDQ0bftQ/3iWSSoGjsDljh9bKz1eVL911KeUGO+t/9IkB6LtZghdbIlnGISbgrVGoEOtGHi0t8uD2Vh/CRyBe+XnQV3HQtkjddLQitAesKTYunK1Ctia3x7klVjRH9XiJ11q6IbR8gz7rchdHYZe6HP+w/LyWMS5z6M26AXQrVw=="]}';

# pat - queryactivated
export INVOKE_CC_NAME="pat";
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n $INVOKE_CC_NAME --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"function":"queryactivated","Args":["0x333c60b9f1878234cddf68cbc2ba431ddc41d7bcb035b4111c9f2f817da3126"]}';

# rreg - create
export INVOKE_CC_NAME="rreg";
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n $INVOKE_CC_NAME --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"function":"invoke","Args":["0x333c60b9f1878234cddf68cbc2ba431ddc41d7bcb035b4111c9f2f817da3126","read,write","description","iconuri","name","type","1595230979","vF9Oyfm+G9qS4/Qfns5MgSZNYjOPlAIZVECh2I5Z7HHgdloy5q7gJoxi7c1S2/ebIQbEMLS05x3+b0WD0VJfcWSUwZMHr3jfXYYwbeZ1TerKpvfp1j21nZ+OEP26bc28rLRAYZsVQ4Ilx7qp+uLfxu9X9x37Qj3n0CI2TEiKYSSYDQ0bftQ/3iWSSoGjsDljh9bKz1eVL911KeUGO+t/9IkB6LtZghdbIlnGISbgrVGoEOtGHi0t8uD2Vh/CRyBe+XnQV3HQtkjddLQitAesKTYunK1Ctia3x7klVjRH9XiJ11q6IbR8gz7rchdHYZe6HP+w/LyWMS5z6M26AXQrVw=="]}';



export INVOKE_CC_NAME="pat";
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n $INVOKE_CC_NAME --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c '{"function":"queryactivated","Args":["0x333c60b9f1878234cddf68cbc2ba431ddc41d7bcb035b4111c9f2f817da3126"]}';

