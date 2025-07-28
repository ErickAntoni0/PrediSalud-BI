const hre = require("hardhat");

async function main() {
  console.log("🏥 Desplegando contratos médicos...");

  // Desplegar MedicalRecords
  const MedicalRecords = await hre.ethers.getContractFactory("MedicalRecords");
  const medicalRecords = await MedicalRecords.deploy();
  await medicalRecords.waitForDeployment();
  console.log("✅ MedicalRecords desplegado en:", await medicalRecords.getAddress());

  // Desplegar PatientConsent
  const PatientConsent = await hre.ethers.getContractFactory("PatientConsent");
  const patientConsent = await PatientConsent.deploy();
  await patientConsent.waitForDeployment();
  console.log("✅ PatientConsent desplegado en:", await patientConsent.getAddress());

  // Desplegar MedicalAudit
  const MedicalAudit = await hre.ethers.getContractFactory("MedicalAudit");
  const medicalAudit = await MedicalAudit.deploy();
  await medicalAudit.waitForDeployment();
  console.log("✅ MedicalAudit desplegado en:", await medicalAudit.getAddress());

  console.log("\n🎉 Todos los contratos médicos desplegados exitosamente!");
  console.log("\n📋 Direcciones de contratos:");
  console.log("MedicalRecords:", await medicalRecords.getAddress());
  console.log("PatientConsent:", await patientConsent.getAddress());
  console.log("MedicalAudit:", await medicalAudit.getAddress());

  // Guardar las direcciones en un archivo para uso posterior
  const fs = require('fs');
  const contractAddresses = {
    MedicalRecords: await medicalRecords.getAddress(),
    PatientConsent: await patientConsent.getAddress(),
    MedicalAudit: await medicalAudit.getAddress(),
    network: hre.network.name
  };

  fs.writeFileSync(
    'contract-addresses.json',
    JSON.stringify(contractAddresses, null, 2)
  );
  console.log("\n💾 Direcciones guardadas en contract-addresses.json");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  }); 