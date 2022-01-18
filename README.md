1. Run the first node: `flask run --port 5000`

2. Run the second node: `flask run --port 5001`

3. Register nodes:
```bash
curl -X POST \
  http://127.0.0.1:5000/nodes/register -H 'content-type: application/json' \
  -d '{
	"nodes": ["http://127.0.0.1:5001"]
}'
```
```bash
curl -X POST \
  http://127.0.0.1:5001/nodes/register -H 'content-type: application/json' \
  -d '{
	"nodes": ["http://127.0.0.1:5000"]
}'
```
4. Mine on first node:
```bash
curl -X GET http://127.0.0.1:5000/mine 
```
5. Run resolve conflict on each node:
```bash
curl -X GET http://127.0.0.1:5000/nodes/resolve

curl -X GET http://127.0.0.1:5001/nodes/resolve
```


Example of response:
```json
{
    "chain": [
        {
            "index": 0,
            "previous_hash": "1",
            "proof": "100",
            "timestamp": 1642534519.8674047,
            "transactions": []
        },
        {
            "index": 1,
            "previous_hash": "a884b8cd18709b887885d9cfc7d5cce45ee013baa04519c38df96ffafa5e8481",
            "proof": "35293",
            "timestamp": 1642534525.969935,
            "transactions": [
                {
                    "amount": 1,
                    "recipient": "be98b78ccd1c47ffb381370258e968d1",
                    "sender": "0"
                }
            ]
        },
        {
            "index": 2,
            "previous_hash": "1bf73d41103bf90527ed6446de7317d06c683098d5170f54c71f1fa706eb0cf3",
            "proof": "35089",
            "timestamp": 1642534586.6501224,
            "transactions": [
                {
                    "amount": 1,
                    "recipient": "5ced888d7a334982aa81e77875da03cd",
                    "sender": "0"
                }
            ]
        },
        {
            "index": 3,
            "previous_hash": "8630b3af0518f2fd514bf43dfc0a0be2b3a7e1a940c8aac6024692e6792f26ba",
            "proof": "119678",
            "timestamp": 1642534588.2724032,
            "transactions": [
                {
                    "amount": 1,
                    "recipient": "5ced888d7a334982aa81e77875da03cd",
                    "sender": "0"
                }
            ]
        },
        {
            "index": 4,
            "previous_hash": "ff95e69527f2ecf9fce44e25fd23549a9c99b955fed56237f87a1bdd19db1a7b",
            "proof": "146502",
            "timestamp": 1642534588.7228513,
            "transactions": [
                {
                    "amount": 1,
                    "recipient": "5ced888d7a334982aa81e77875da03cd",
                    "sender": "0"
                }
            ]
        },
        {
            "index": 5,
            "previous_hash": "91c7e2d755e3dde4266fcbc1196a0b3721a44c5d14bbe5e7d668ad4a25119aee",
            "proof": "43538",
            "timestamp": 1642534588.987871,
            "transactions": [
                {
                    "amount": 1,
                    "recipient": "5ced888d7a334982aa81e77875da03cd",
                    "sender": "0"
                }
            ]
        },
        {
            "index": 6,
            "previous_hash": "bf2aaf2381cac4e28c2d27cd9b4094454e837549cc1e078b75f9a1e72d2193ad",
            "proof": "85724",
            "timestamp": 1642534589.5554342,
            "transactions": [
                {
                    "amount": 1,
                    "recipient": "5ced888d7a334982aa81e77875da03cd",
                    "sender": "0"
                }
            ]
        },
        {
            "index": 7,
            "previous_hash": "d1e40562fea112a0d06d4c5ce2b6a1258b53924ebc24fb0d4cc1e39795583797",
            "proof": "51178",
            "timestamp": 1642534940.4772842,
            "transactions": [
                {
                    "amount": 1,
                    "recipient": "5ced888d7a334982aa81e77875da03cd",
                    "sender": "0"
                }
            ]
        }
    ],
    "message": "Our chain is authoritative"
}
```