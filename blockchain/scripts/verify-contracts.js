const { ethers } = require("hardhat");
const fs = require("fs");

async function main() {
  console.log("🔍 Verificando contratos desplegados...");

  try {
    // Leer las direcciones de los contratos
    const addresses = JSON.parse(fs.readFileSync("contract-addresses-sepolia.json", "utf8"));
    
    console.log("\n📋 Contratos desplegados en Sepolia:");
    console.log("=====================================");
    console.log(`MedicalRecords: ${addresses.MedicalRecords}`);
    console.log(`PatientConsent: ${addresses.PatientConsent}`);
    console.log(`MedicalAudit: ${addresses.MedicalAudit}`);
    
    console.log("\n🔗 Enlaces de Etherscan:");
    console.log("==========================");
    console.log(`MedicalRecords: https://sepolia.etherscan.io/address/${addresses.MedicalRecords}`);
    console.log(`PatientConsent: https://sepolia.etherscan.io/address/${addresses.PatientConsent}`);
    console.log(`MedicalAudit: https://sepolia.etherscan.io/address/${addresses.MedicalAudit}`);
    
    // Verificar que los contratos existen
    const provider = new ethers.JsonRpcProvider(process.env.SEPOLIA_URL);
    
    console.log("\n✅ Verificando existencia de contratos...");
    
    for (const [name, address] of Object.entries(addresses)) {
      if (name !== 'network') {
        const code = await provider.getCode(address);
        if (code !== "0x") {
          console.log(`✅ ${name}: Contrato válido`);
        } else {
          console.log(`❌ ${name}: Contrato no encontrado`);
        }
      }
    }
    
    console.log("\n🎉 Verificación completada!");
    
  } catch (error) {
    console.error("❌ Error verificando contratos:", error.message);
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  }); 