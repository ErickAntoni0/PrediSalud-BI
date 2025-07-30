# Integración de Contratos Inteligentes y Web3 en MegaMarket BI

## ¿Para qué sirven los contratos inteligentes en este proyecto?

### 1. Transparencia y confianza en la fidelización

- Los **contratos inteligentes** permiten que el programa de puntos de clientes sea **transparente, auditable y sin manipulación**.
- Cada vez que un cliente gana o canjea puntos, la transacción queda registrada en la blockchain, donde **nadie puede alterarla**.

### 2. Automatización de reglas de negocio

- Las reglas de otorgamiento y canje de puntos están **programadas en el contrato** (por ejemplo, solo el owner puede otorgar puntos, los clientes solo pueden canjear si tienen saldo suficiente).
- Esto elimina errores humanos y fraudes.

### 3. Interoperabilidad y expansión

- Los puntos pueden ser usados en otras plataformas, apps o incluso convertidos en tokens, gracias a la naturaleza abierta de la blockchain.

---

## ¿Cómo funcionaría Web3 en la solución?

### 1. Integración backend (Python/FastAPI)

- Usando **web3.py**, el backend puede:
  - Consultar el saldo de puntos de un cliente en la blockchain.
  - Otorgar puntos a un cliente (por ejemplo, después de una compra).
  - Permitir que un cliente canjee puntos por recompensas.

### 2. Integración frontend (opcional)

- Una app web o móvil puede usar **web3.js** o **ethers.js** para que el cliente vea y gestione sus puntos directamente desde su wallet (MetaMask, etc.).

### 3. Flujo típico en la demo

1. **Compra registrada en Snowflake**
2. **API detecta compra y llama a Web3**
3. **Contrato inteligente otorga puntos al cliente**
4. **Cliente puede consultar/canjear puntos desde la app o dashboard**
5. **Todo queda registrado en la blockchain, visible y auditable**

---

## ¿Por qué es innovador para MegaMarket?

- **Confianza:** Los clientes pueden verificar sus puntos en la blockchain.
- **Automatización:** Sin intervención manual, sin errores.
- **Expansión:** El sistema puede integrarse con otras tiendas, apps o partners en el futuro.

---

## Comandos útiles para la demo

### 1. Compilar el contrato

```bash
npx hardhat compile
```

### 2. Ejecutar pruebas automáticas

```bash
npx hardhat test
```

### 3. Desplegar el contrato en Sepolia

```bash
npx hardhat run scripts/deploy.js --network sepolia
```

### 4. Verificar el contrato en Etherscan (opcional)

- Haz clic en "Verify and Publish" en Etherscan y sigue el asistente.

### 5. Consultar el contrato en Etherscan

- Ve a: https://sepolia.etherscan.io/address/[DIRECCION_DEL_CONTRATO]

### 6. (Opcional) Interactuar con el contrato desde Python

```python
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/TU_API_KEY'))
contract = w3.eth.contract(address='DIRECCION_DEL_CONTRATO', abi=ABI)
# Consultar puntos
contract.functions.getPoints('DIRECCION_CLIENTE').call()
```
