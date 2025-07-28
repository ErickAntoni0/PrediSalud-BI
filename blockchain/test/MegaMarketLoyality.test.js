const { expect } = require("chai");

describe("MegaMarketLoyalty", function () {
  let loyalty, owner, addr1, addr2;

  beforeEach(async function () {
    const Loyalty = await ethers.getContractFactory("MegaMarketLoyalty");
    [owner, addr1, addr2] = await ethers.getSigners();
    loyalty = await Loyalty.deploy();
  });

  it("El owner puede otorgar puntos", async function () {
    await loyalty.awardPoints(addr1.address, 100);
    expect(await loyalty.getPoints(addr1.address)).to.equal(100);
  });

  it("Un cliente puede canjear puntos si tiene suficientes", async function () {
    await loyalty.awardPoints(addr1.address, 200);
    await loyalty.connect(addr1).redeemPoints(150);
    expect(await loyalty.getPoints(addr1.address)).to.equal(50);
  });

  it("No permite canjear más puntos de los que tiene", async function () {
    await loyalty.awardPoints(addr1.address, 50);
    await expect(
      loyalty.connect(addr1).redeemPoints(100)
    ).to.be.revertedWith("Not enough points");
  });

  it("Solo el owner puede otorgar puntos", async function () {
    await expect(
      loyalty.connect(addr1).awardPoints(addr2.address, 100)
    ).to.be.revertedWith("Not owner");
  });
});