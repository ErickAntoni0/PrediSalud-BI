async function main() {
  const MegaMarketLoyalty = await ethers.getContractFactory("MegaMarketLoyalty");
  const contract = await MegaMarketLoyalty.deploy();
  await contract.waitForDeployment();
  console.log("MegaMarketLoyalty deployed to:", await contract.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});