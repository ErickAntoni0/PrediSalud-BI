const { ethers } = require("hardhat");
const fs = require("fs");

async function main() {
  console.log("🏥 Interactuando con contratos médicos...");

  try {
    // Leer las direcciones de los contratos
    const addresses = JSON.parse(fs.readFileSync("contract-addresses-sepolia.json", "utf8"));
    
    // Obtener el signer
    const [signer] = await ethers.getSigners();
    console.log("👤 Cuenta conectada:", await signer.getAddress());
    
    // Conectar a los contratos
    const MedicalRecords = await ethers.getContractFactory("MedicalRecords");
    const medicalRecords = MedicalRecords.attach(addresses.MedicalRecords);
    
    const PatientConsent = await ethers.getContractFactory("PatientConsent");
    const patientConsent = PatientConsent.attach(addresses.PatientConsent);
    
    const MedicalAudit = await ethers.getContractFactory("MedicalAudit");
    const medicalAudit = MedicalAudit.attach(addresses.MedicalAudit);
    
    console.log("\n📋 Información de contratos:");
    console.log("==============================");
    console.log(`MedicalRecords: ${addresses.MedicalRecords}`);
    console.log(`PatientConsent: ${addresses.PatientConsent}`);
    console.log(`MedicalAudit: ${addresses.MedicalAudit}`);
    
    // Ejemplos de interacción con MedicalRecords
    console.log("\n🔬 Probando MedicalRecords...");
    
    // Agregar un registro médico
    const patientId = "P001";
    const diagnosis = "Gripe";
    const treatment = "Paracetamol";
    const timestamp = Math.floor(Date.now() / 1000);
    
    console.log(`📝 Agregando registro para paciente ${patientId}...`);
    const tx1 = await medicalRecords.createMedicalRecord(patientId, diagnosis, treatment);
    await tx1.wait();
    console.log("✅ Registro médico agregado");
    
    // Obtener el registro usando el hash del evento
    console.log(`🔍 Obteniendo registro para paciente ${patientId}...`);
    const receipt = await tx1.wait();
    const recordHash = receipt.logs[0].topics[1]; // Obtener el hash del evento
    const record = await medicalRecords.getMedicalRecord(recordHash);
    console.log("📋 Registro médico:", {
      patientId: record.patientId,
      diagnosis: record.diagnosis,
      treatment: record.treatment,
      timestamp: new Date(Number(record.timestamp) * 1000).toLocaleString()
    });
    
    // Ejemplos de interacción con PatientConsent
    console.log("\n✅ Probando PatientConsent...");
    
    // Dar consentimiento
    const patientAddress = await signer.getAddress();
    const dataSharing = true;
    const researchParticipation = false;
    const emergencyAccess = true;
    
    console.log(`📋 Actualizando consentimiento para ${patientAddress}...`);
    const tx2 = await patientConsent.updateConsent(dataSharing, researchParticipation, emergencyAccess);
    await tx2.wait();
    console.log("✅ Consentimiento actualizado");
    
    // Verificar consentimiento
    console.log(`🔍 Verificando consentimiento para ${patientAddress}...`);
    const consent = await patientConsent.getConsent(patientAddress);
    console.log("📋 Consentimiento:", {
      dataSharing: consent.dataSharing ? "Sí" : "No",
      researchParticipation: consent.researchParticipation ? "Sí" : "No",
      emergencyAccess: consent.emergencyAccess ? "Sí" : "No",
      lastUpdated: new Date(Number(consent.lastUpdated) * 1000).toLocaleString(),
      patient: consent.patientAddr
    });
    
    // Ejemplos de interacción con MedicalAudit
    console.log("\n🔍 Probando MedicalAudit...");
    
    // Agregar auditoría
    const action = "Access";
    const details = "Patient record accessed";
    const auditRecordHash = "0x0000000000000000000000000000000000000000000000000000000000000000";
    
    console.log(`📊 Creando auditoría...`);
    const tx3 = await medicalAudit.createAuditLog(action, details, auditRecordHash);
    await tx3.wait();
    console.log("✅ Auditoría creada");
    
    // Obtener auditoría usando el hash del evento
    const receipt3 = await tx3.wait();
    const logHash = receipt3.logs[0].topics[1]; // Obtener el hash del evento
    const audit = await medicalAudit.getAuditLog(logHash);
    console.log("📊 Auditoría:", {
      user: audit.user,
      action: audit.action,
      details: audit.details,
      timestamp: new Date(Number(audit.timestamp) * 1000).toLocaleString(),
      recordHash: audit.recordHash
    });
    
    console.log("\n🎉 Interacciones completadas exitosamente!");
    
  } catch (error) {
    console.error("❌ Error interactuando con contratos:", error.message);
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  }); 