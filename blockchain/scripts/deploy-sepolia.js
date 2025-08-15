const { ethers } = require("hardhat");

async function main() {
  console.log("🚀 Desplegando contratos en Sepolia...");

  // Desplegar MedicalRecords
  const MedicalRecords = await ethers.getContractFactory("MedicalRecords");
  const medicalRecords = await MedicalRecords.deploy();
  await medicalRecords.waitForDeployment();
  const medicalRecordsAddress = await medicalRecords.getAddress();
  console.log("✅ MedicalRecords desplegado en:", medicalRecordsAddress);

  // Desplegar PatientConsent
  const PatientConsent = await ethers.getContractFactory("PatientConsent");
  const patientConsent = await PatientConsent.deploy();
  await patientConsent.waitForDeployment();
  const patientConsentAddress = await patientConsent.getAddress();
  console.log("✅ PatientConsent desplegado en:", patientConsentAddress);

  // Desplegar MedicalAudit
  const MedicalAudit = await ethers.getContractFactory("MedicalAudit");
  const medicalAudit = await MedicalAudit.deploy();
  await medicalAudit.waitForDeployment();
  const medicalAuditAddress = await medicalAudit.getAddress();
  console.log("✅ MedicalAudit desplegado en:", medicalAuditAddress);

  // Guardar direcciones en archivo
  const fs = require("fs");
  const addresses = {
    MedicalRecords: medicalRecordsAddress,
    PatientConsent: patientConsentAddress,
    MedicalAudit: medicalAuditAddress,
    network: "sepolia"
  };

  fs.writeFileSync(
    "contract-addresses-sepolia.json",
    JSON.stringify(addresses, null, 2)
  );

  console.log("\n📋 Direcciones guardadas en: blockchain/contract-addresses-sepolia.json");
  console.log("\n🔗 Verificar en Etherscan:");
  console.log(`MedicalRecords: https://sepolia.etherscan.io/address/${medicalRecordsAddress}`);
  console.log(`PatientConsent: https://sepolia.etherscan.io/address/${patientConsentAddress}`);
  console.log(`MedicalAudit: https://sepolia.etherscan.io/address/${medicalAuditAddress}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Error desplegando contratos:", error);
    process.exit(1);
  }); 