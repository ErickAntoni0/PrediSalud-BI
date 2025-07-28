const { ethers } = require("hardhat");

async function main() {
  console.log("🔍 Verificando conexión a Sepolia...");
  
  try {
    // Verificar conexión
    const provider = ethers.provider;
    const network = await provider.getNetwork();
    console.log("✅ Conectado a red:", network.name);
    
    // Verificar balance
    const [signer] = await ethers.getSigners();
    const balance = await signer.getBalance();
    console.log("💰 Balance:", ethers.formatEther(balance), "ETH");
    
    if (balance < ethers.parseEther("0.01")) {
      console.log("⚠️ Balance bajo. Necesitas ETH para desplegar contratos.");
      console.log("💡 Obtén ETH de prueba en: https://sepoliafaucet.com/");
      return;
    }
    
    console.log("\n🚀 Desplegando contratos...");
    
    // Desplegar MedicalRecords
    const MedicalRecords = await ethers.getContractFactory("MedicalRecords");
    console.log("📝 Desplegando MedicalRecords...");
    const medicalRecords = await MedicalRecords.deploy();
    await medicalRecords.waitForDeployment();
    const medicalRecordsAddress = await medicalRecords.getAddress();
    console.log("✅ MedicalRecords:", medicalRecordsAddress);
    
    // Desplegar PatientConsent
    const PatientConsent = await ethers.getContractFactory("PatientConsent");
    console.log("📝 Desplegando PatientConsent...");
    const patientConsent = await PatientConsent.deploy();
    await patientConsent.waitForDeployment();
    const patientConsentAddress = await patientConsent.getAddress();
    console.log("✅ PatientConsent:", patientConsentAddress);
    
    // Desplegar MedicalAudit
    const MedicalAudit = await ethers.getContractFactory("MedicalAudit");
    console.log("📝 Desplegando MedicalAudit...");
    const medicalAudit = await MedicalAudit.deploy();
    await medicalAudit.waitForDeployment();
    const medicalAuditAddress = await medicalAudit.getAddress();
    console.log("✅ MedicalAudit:", medicalAuditAddress);
    
    // Guardar direcciones
    const fs = require("fs");
    const addresses = {
      MedicalRecords: medicalRecordsAddress,
      PatientConsent: patientConsentAddress,
      MedicalAudit: medicalAuditAddress,
      network: "sepolia",
      deployedAt: new Date().toISOString()
    };
    
    fs.writeFileSync(
      "blockchain/contract-addresses-sepolia.json",
      JSON.stringify(addresses, null, 2)
    );
    
    console.log("\n📋 Direcciones guardadas en: blockchain/contract-addresses-sepolia.json");
    console.log("\n🔗 Verificar en Etherscan:");
    console.log(`MedicalRecords: https://sepolia.etherscan.io/address/${medicalRecordsAddress}`);
    console.log(`PatientConsent: https://sepolia.etherscan.io/address/${patientConsentAddress}`);
    console.log(`MedicalAudit: https://sepolia.etherscan.io/address/${medicalAuditAddress}`);
    
  } catch (error) {
    console.error("❌ Error:", error.message);
    if (error.message.includes("insufficient funds")) {
      console.log("💡 Necesitas ETH de prueba. Obtén en: https://sepoliafaucet.com/");
    }
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Error fatal:", error);
    process.exit(1);
  }); 